import csv
import io
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.cache.redis_client import cache_get, cache_set, make_cache_key
from backend.connectors import ctgov
from backend.db.database import get_db
from backend.db.models import Trial
from backend.schemas.trial import TrialDetail, TrialSearchResult, TrialSummary

router = APIRouter(prefix="/trials", tags=["trials"])
logger = logging.getLogger(__name__)


def _data_to_summary(data: dict) -> TrialSummary:
    return TrialSummary(
        nct_id=data["nct_id"],
        title=data.get("title", ""),
        sponsor_name=data.get("sponsor_name"),
        sponsor_type=data.get("sponsor_type"),
        phase=data.get("phase"),
        status=data.get("status"),
        conditions=data.get("conditions") or [],
        countries=data.get("countries") or [],
        enrollment=data.get("enrollment"),
        start_date=data.get("start_date"),
        primary_completion_date=data.get("primary_completion_date"),
        composite_score=None,
    )


def _orm_to_summary(trial: Trial) -> TrialSummary:
    return TrialSummary(
        nct_id=trial.nct_id,
        title=trial.title,
        sponsor_name=trial.sponsor_name,
        sponsor_type=trial.sponsor_type,
        phase=trial.phase,
        status=trial.status,
        conditions=trial.conditions or [],
        countries=trial.countries or [],
        enrollment=trial.enrollment,
        start_date=str(trial.start_date) if trial.start_date else None,
        primary_completion_date=str(trial.primary_completion_date)
        if trial.primary_completion_date
        else None,
        composite_score=None,
    )


async def _upsert_trial(db: AsyncSession, data: dict) -> Trial | None:
    """Insert or update a trial row. Returns None on any DB error."""
    try:
        result = await db.execute(select(Trial).where(Trial.nct_id == data["nct_id"]))
        trial = result.scalar_one_or_none()

        fields = {
            "title": data.get("title", ""),
            "sponsor_name": data.get("sponsor_name"),
            "sponsor_type": data.get("sponsor_type"),
            "phase": data.get("phase"),
            "status": data.get("status"),
            "conditions": data.get("conditions"),
            "interventions": data.get("interventions"),
            "countries": data.get("countries"),
            "enrollment": data.get("enrollment"),
            "enrollment_type": data.get("enrollment_type"),
            "start_date": data.get("start_date"),
            "primary_completion_date": data.get("primary_completion_date"),
            "source": data.get("source", "ctgov"),
            "raw_json": data.get("raw_json"),
        }

        if trial is None:
            trial = Trial(nct_id=data["nct_id"], **fields)
            db.add(trial)
        else:
            for k, v in fields.items():
                setattr(trial, k, v)

        await db.commit()
        await db.refresh(trial)
        return trial
    except Exception as exc:
        logger.warning("DB upsert failed for %s: %s", data.get("nct_id"), exc)
        return None


@router.get("/search", response_model=TrialSearchResult)
async def search_trials(
    db: Annotated[AsyncSession | None, Depends(get_db)],
    therapy_area: str | None = Query(None, description="MeSH term or free text"),
    phase: list[str] | None = Query(None, description="1|2|3|4|early1"),
    status: str | None = Query("recruiting", description="recruiting|active|completed|all"),
    country: str | None = Query(None, description="Country name or ISO code"),
    drug_type: str | None = Query(None, description="small_molecule|biologic|..."),
    sponsor_type: str | None = Query(None, description="industry|academic|nih|all"),
    start_date_from: str | None = Query(None),
    start_date_to: str | None = Query(None),
    min_score: int | None = Query(None, ge=0, le=100),
    sort_by: str = Query("start_date"),
    sort_order: str = Query("desc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
) -> TrialSearchResult:
    cache_key = make_cache_key("search", {
        "therapy_area": therapy_area, "phase": phase, "status": status,
        "country": country, "drug_type": drug_type, "page": page, "per_page": per_page,
    })
    cached = await cache_get(cache_key)
    if cached:
        return TrialSearchResult(**cached)

    try:
        raw = await ctgov.search_trials(
            query=therapy_area,
            phases=phase,
            status=status,
            country=country,
            drug_type=drug_type,
            page_size=per_page,
        )
    except Exception as exc:
        logger.error("ClinicalTrials.gov API error: %s", exc)
        raise HTTPException(status_code=502, detail="Error fetching trials from ClinicalTrials.gov")

    trials_out: list[TrialSummary] = []
    for trial_data in raw["trials"]:
        if db is not None:
            orm = await _upsert_trial(db, trial_data)
            trials_out.append(_orm_to_summary(orm) if orm else _data_to_summary(trial_data))
        else:
            trials_out.append(_data_to_summary(trial_data))

    result = TrialSearchResult(
        trials=trials_out,
        total_count=raw["total_count"],
        page=page,
        per_page=per_page,
        next_page_token=raw.get("next_page_token"),
    )
    await cache_set(cache_key, result.model_dump())
    return result


@router.get("/mesh-autocomplete")
async def mesh_autocomplete(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=20),
) -> list[dict]:
    cache_key = make_cache_key("mesh", {"q": q.lower(), "limit": limit})
    cached = await cache_get(cache_key)
    if cached:
        return cached

    suggestions = await ctgov.mesh_autocomplete(q, limit=limit)
    await cache_set(cache_key, suggestions, ttl=604800)
    return suggestions


@router.get("/export/csv")
async def export_csv(
    therapy_area: str | None = Query(None),
    phase: list[str] | None = Query(None),
    status: str | None = Query("recruiting"),
    country: str | None = Query(None),
) -> StreamingResponse:
    try:
        raw = await ctgov.search_trials(
            query=therapy_area, phases=phase, status=status,
            country=country, page_size=100,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "nct_id", "title", "sponsor_name", "phase", "status",
        "conditions", "countries", "enrollment", "start_date", "primary_completion_date",
    ])
    writer.writeheader()
    for t in raw["trials"]:
        writer.writerow({
            "nct_id": t.get("nct_id", ""),
            "title": t.get("title", ""),
            "sponsor_name": t.get("sponsor_name", ""),
            "phase": t.get("phase", ""),
            "status": t.get("status", ""),
            "conditions": "; ".join(t.get("conditions") or []),
            "countries": "; ".join(t.get("countries") or []),
            "enrollment": t.get("enrollment", ""),
            "start_date": t.get("start_date", ""),
            "primary_completion_date": t.get("primary_completion_date", ""),
        })

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=pharmalens_trials.csv"},
    )


@router.get("/{nct_id}", response_model=TrialDetail)
async def get_trial(
    nct_id: str,
    db: Annotated[AsyncSession | None, Depends(get_db)],
) -> TrialDetail:
    cache_key = make_cache_key("trial", {"nct_id": nct_id})
    cached = await cache_get(cache_key)
    if cached:
        return TrialDetail(**cached)

    # Try DB first (only if available)
    if db is not None:
        try:
            result = await db.execute(select(Trial).where(Trial.nct_id == nct_id.upper()))
            orm = result.scalar_one_or_none()
            if orm is not None:
                out = _build_detail_from_orm(orm)
                await cache_set(cache_key, out.model_dump())
                return out
        except Exception as exc:
            logger.warning("DB lookup failed for %s: %s", nct_id, exc)

    # Fall back to API
    try:
        data = await ctgov.get_trial(nct_id.upper())
    except Exception as exc:
        logger.error("ClinicalTrials.gov error for %s: %s", nct_id, exc)
        raise HTTPException(status_code=502, detail="Error fetching trial")

    if data is None:
        raise HTTPException(status_code=404, detail=f"Trial {nct_id} not found")

    if db is not None:
        orm = await _upsert_trial(db, data)
        if orm is not None:
            out = _build_detail_from_orm(orm)
            await cache_set(cache_key, out.model_dump())
            return out

    out = _build_detail_from_data(data)
    await cache_set(cache_key, out.model_dump())
    return out


def _build_detail_from_orm(trial: Trial) -> TrialDetail:
    raw = trial.raw_json or {}
    proto = raw.get("protocolSection", {})
    return TrialDetail(
        nct_id=trial.nct_id,
        title=trial.title,
        sponsor_name=trial.sponsor_name,
        sponsor_type=trial.sponsor_type,
        phase=trial.phase,
        status=trial.status,
        conditions=trial.conditions or [],
        countries=trial.countries or [],
        enrollment=trial.enrollment,
        enrollment_type=trial.enrollment_type,
        start_date=str(trial.start_date) if trial.start_date else None,
        primary_completion_date=str(trial.primary_completion_date)
        if trial.primary_completion_date else None,
        interventions=trial.interventions,
        brief_summary=proto.get("descriptionModule", {}).get("briefSummary"),
        primary_outcomes=proto.get("outcomesModule", {}).get("primaryOutcomes", []),
    )


def _build_detail_from_data(data: dict) -> TrialDetail:
    raw = data.get("raw_json") or {}
    proto = raw.get("protocolSection", {})
    return TrialDetail(
        nct_id=data["nct_id"],
        title=data.get("title", ""),
        sponsor_name=data.get("sponsor_name"),
        sponsor_type=data.get("sponsor_type"),
        phase=data.get("phase"),
        status=data.get("status"),
        conditions=data.get("conditions") or [],
        countries=data.get("countries") or [],
        enrollment=data.get("enrollment"),
        enrollment_type=data.get("enrollment_type"),
        start_date=data.get("start_date"),
        primary_completion_date=data.get("primary_completion_date"),
        interventions=data.get("interventions"),
        brief_summary=data.get("brief_summary")
            or proto.get("descriptionModule", {}).get("briefSummary"),
        primary_outcomes=data.get("primary_outcomes")
            or proto.get("outcomesModule", {}).get("primaryOutcomes", []),
    )
