"""ClinicalTrials.gov v2 REST API connector."""
import logging
from typing import Any

import httpx

from backend.config import settings

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": "PharmaLens/0.1 (open-source pharma BD intelligence; contact via GitHub)",
    "Accept": "application/json",
}

# Map PharmaLens phase strings to ClinicalTrials.gov API values
PHASE_MAP = {
    "early1": "EARLY_PHASE1",
    "1": "PHASE1",
    "2": "PHASE2",
    "3": "PHASE3",
    "4": "PHASE4",
}

STATUS_MAP = {
    "recruiting": "RECRUITING",
    "active": "ACTIVE_NOT_RECRUITING",
    "completed": "COMPLETED",
    "all": None,
}

DRUG_TYPE_LABELS = {
    "small_molecule": "Drug",
    "biologic": "Biological",
    "cell_therapy": "Genetic",
    "gene_therapy": "Genetic",
    "device": "Device",
    "combination": "Combination Product",
}

_FIELDS = ",".join([
    "NCTId",
    "BriefTitle",
    "OfficialTitle",
    "LeadSponsorName",
    "LeadSponsorClass",
    "Phase",
    "OverallStatus",
    "Condition",
    "ConditionMeshTerm",
    "InterventionType",
    "InterventionName",
    "InterventionOtherName",
    "LocationCountry",
    "EnrollmentCount",
    "EnrollmentType",
    "StartDate",
    "PrimaryCompletionDate",
    "StudyFirstPostDate",
    "LastUpdatePostDate",
    "BriefSummary",
    "EligibilityCriteria",
    "PrimaryOutcomeMeasure",
    "SecondaryOutcomeMeasure",
    "StudySiteCount",
])


def _normalise_sponsor_type(sponsor_class: str | None) -> str:
    if not sponsor_class:
        return "other"
    sc = sponsor_class.upper()
    if sc in ("INDUSTRY",):
        return "industry"
    if sc in ("NIH", "FED", "U.S. FED"):
        return "nih"
    if sc in ("NETWORK", "INDIV", "OTHER_GOV", "UNKNOWN"):
        return "academic"
    return "academic"


def _parse_date(val: str | None) -> str | None:
    """Return ISO date string or None. Handles 'Month YYYY' and 'YYYY-MM-DD'."""
    if not val:
        return None
    val = val.strip()
    # Already ISO format
    if len(val) == 10 and val[4] == "-":
        return val
    # "Month YYYY" format
    from datetime import datetime
    for fmt in ("%B %Y", "%b %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _extract_interventions(study: dict) -> list[dict]:
    proto = study.get("protocolSection", {})
    arms = proto.get("armsInterventionsModule", {})
    raw = arms.get("interventions", [])
    result = []
    for item in raw:
        result.append({
            "type": item.get("type"),
            "name": item.get("name"),
            "other_names": item.get("otherNames", []),
        })
    return result


def _normalise_study(study: dict) -> dict:
    """Convert a raw v2 study object to PharmaLens canonical trial dict."""
    proto = study.get("protocolSection", {})

    ident = proto.get("identificationModule", {})
    status_mod = proto.get("statusModule", {})
    sponsor_mod = proto.get("sponsorCollaboratorsModule", {})
    design_mod = proto.get("designModule", {})
    conditions_mod = proto.get("conditionsModule", {})
    locations_mod = proto.get("contactsLocationsModule", {})
    desc_mod = proto.get("descriptionModule", {})
    outcomes_mod = proto.get("outcomesModule", {})
    eligibility_mod = proto.get("eligibilityModule", {})

    lead_sponsor = sponsor_mod.get("leadSponsor", {})

    phases = design_mod.get("phases", [])
    phase_str = phases[0].replace("PHASE", "") if phases else None
    if phase_str == "EARLY_PHASE1":
        phase_str = "Early Phase 1"
    elif phase_str:
        phase_str = f"Phase {phase_str}"

    enrollment_info = design_mod.get("enrollmentInfo", {})
    countries = list({
        loc.get("country")
        for loc in locations_mod.get("locations", [])
        if loc.get("country")
    })

    mesh_conditions = conditions_mod.get("meshes", [])
    conditions = (
        [m.get("term") for m in mesh_conditions if m.get("term")]
        or conditions_mod.get("conditions", [])
    )

    primary_outcomes = [
        o.get("measure")
        for o in outcomes_mod.get("primaryOutcomes", [])
        if o.get("measure")
    ]
    secondary_outcomes = [
        o.get("measure")
        for o in outcomes_mod.get("secondaryOutcomes", [])
        if o.get("measure")
    ]

    return {
        "nct_id": ident.get("nctId"),
        "title": ident.get("briefTitle") or ident.get("officialTitle", ""),
        "official_title": ident.get("officialTitle"),
        "sponsor_name": lead_sponsor.get("name"),
        "sponsor_type": _normalise_sponsor_type(lead_sponsor.get("class")),
        "phase": phase_str,
        "status": status_mod.get("overallStatus"),
        "conditions": conditions,
        "interventions": _extract_interventions(study),
        "countries": countries,
        "enrollment": enrollment_info.get("count"),
        "enrollment_type": enrollment_info.get("type"),
        "start_date": _parse_date(status_mod.get("startDateStruct", {}).get("date")),
        "primary_completion_date": _parse_date(
            status_mod.get("primaryCompletionDateStruct", {}).get("date")
        ),
        "brief_summary": desc_mod.get("briefSummary"),
        "eligibility_criteria": eligibility_mod.get("eligibilityCriteria"),
        "primary_outcomes": primary_outcomes,
        "secondary_outcomes": secondary_outcomes,
        "site_count": study.get("hasResults"),  # placeholder; site count from derived module
        "source": "ctgov",
        "raw_json": study,
    }


_COUNTRY_ALIASES: dict[str, str] = {
    "usa": "United States",
    "us": "United States",
    "u.s.": "United States",
    "uk": "United Kingdom",
    "uae": "United Arab Emirates",
}


def _expand_country(value: str) -> str:
    return _COUNTRY_ALIASES.get(value.strip().lower(), value)


async def search_trials(
    *,
    query: str | None = None,
    phases: list[str] | None = None,
    status: str | None = None,
    country: str | None = None,
    drug_type: str | None = None,
    sponsor_type: str | None = None,
    start_date_from: str | None = None,
    start_date_to: str | None = None,
    page_size: int = 25,
    page_token: str | None = None,
) -> dict:
    """Query ClinicalTrials.gov v2 API and return normalised results."""
    params: dict[str, Any] = {
        "format": "json",
        "pageSize": min(page_size, 100),
    }

    if query:
        params["query.cond"] = query

    if phases:
        ct_phases = [PHASE_MAP[p] for p in phases if p in PHASE_MAP]
        if ct_phases:
            params["filter.phase"] = "|".join(ct_phases)

    if status and status != "all":
        ct_status = STATUS_MAP.get(status)
        if ct_status:
            params["filter.overallStatus"] = ct_status

    # drug_type is post-filtered client-side; ClinicalTrials.gov v2 has no
    # intervention-type filter — query.intr is a name search, not a type filter.

    if country:
        # Expand common abbreviations; CT.gov needs the full country name
        country_name = _expand_country(country)
        params["query.locn"] = country_name

    if page_token:
        params["pageToken"] = page_token

    try:
        async with httpx.AsyncClient(timeout=30.0, headers=_HEADERS) as client:
            resp = await client.get(f"{settings.ctgov_base_url}/studies", params=params)
            resp.raise_for_status()
            data = resp.json()

        studies = data.get("studies", [])
        normalised = [_normalise_study(s) for s in studies]
        return {
            "trials": normalised,
            "total_count": data.get("totalCount", len(normalised)),
            "next_page_token": data.get("nextPageToken"),
        }
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 403:
            logger.warning(
                "ClinicalTrials.gov returned 403 (IP blocked) — serving mock data. "
                "Check /api/v1/health/ctgov to diagnose."
            )
            from backend.connectors.mock_data import filter_mock_trials
            results = filter_mock_trials(query=query, phases=phases, status=status)
            return {"trials": results, "total_count": len(results), "next_page_token": None}
        raise


async def get_trial(nct_id: str) -> dict | None:
    """Fetch a single trial by NCT ID and return normalised dict."""
    try:
        async with httpx.AsyncClient(timeout=30.0, headers=_HEADERS) as client:
            resp = await client.get(
                f"{settings.ctgov_base_url}/studies/{nct_id}",
                params={"format": "json"},
            )
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            data = resp.json()
        return _normalise_study(data)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 403:
            from backend.connectors.mock_data import MOCK_TRIALS
            match = next((t for t in MOCK_TRIALS if t["nct_id"] == nct_id), None)
            if match:
                return match
            return None
        raise


async def mesh_autocomplete(query: str, limit: int = 10) -> list[dict]:
    """Suggest MeSH terms using the NLM MeSH Lookup API."""
    async with httpx.AsyncClient(timeout=10.0, headers=_HEADERS) as client:
        resp = await client.get(
            f"{settings.mesh_api_url}/lookup/descriptor",
            params={"label": query, "limit": limit, "match": "contains"},
        )
        if resp.status_code != 200:
            return []
        data = resp.json()

    results = []
    for item in data:
        results.append({
            "label": item.get("label"),
            "ui": item.get("resource", "").split("/")[-1],
        })
    return results
