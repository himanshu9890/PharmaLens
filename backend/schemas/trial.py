from typing import Any

from pydantic import BaseModel


class TrialSummary(BaseModel):
    nct_id: str
    title: str
    sponsor_name: str | None = None
    sponsor_type: str | None = None
    phase: str | None = None
    status: str | None = None
    conditions: list[str] = []
    countries: list[str] = []
    enrollment: int | None = None
    start_date: str | None = None
    primary_completion_date: str | None = None
    composite_score: float | None = None


class TrialSearchResult(BaseModel):
    trials: list[TrialSummary]
    total_count: int
    page: int
    per_page: int
    next_page_token: str | None = None


class TrialDetail(BaseModel):
    nct_id: str
    title: str
    sponsor_name: str | None = None
    sponsor_type: str | None = None
    phase: str | None = None
    status: str | None = None
    conditions: list[str] = []
    countries: list[str] = []
    enrollment: int | None = None
    enrollment_type: str | None = None
    start_date: str | None = None
    primary_completion_date: str | None = None
    interventions: Any | None = None
    brief_summary: str | None = None
    primary_outcomes: list[Any] = []
    composite_score: float | None = None
    trial_promise_score: float | None = None
    drug_profile_score: float | None = None
    kol_sentiment_score: float | None = None
    competitive_score: float | None = None
