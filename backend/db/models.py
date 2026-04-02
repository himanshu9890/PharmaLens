import uuid
from datetime import date, datetime

from sqlalchemy import ARRAY, Boolean, Date, Integer, Numeric, String, Text
from sqlalchemy import DateTime as SADateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.db.database import Base


class Trial(Base):
    __tablename__ = "trials"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nct_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    sponsor_name: Mapped[str | None] = mapped_column(Text)
    sponsor_type: Mapped[str | None] = mapped_column(String(20))  # industry | academic | other
    phase: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str | None] = mapped_column(String(40), index=True)
    conditions: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    interventions: Mapped[dict | None] = mapped_column(JSONB)
    countries: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    enrollment: Mapped[int | None] = mapped_column(Integer)
    enrollment_type: Mapped[str | None] = mapped_column(String(20))  # Actual | Anticipated
    start_date: Mapped[date | None] = mapped_column(Date)
    primary_completion_date: Mapped[date | None] = mapped_column(Date)
    source: Mapped[str | None] = mapped_column(String(20), default="ctgov")
    raw_json: Mapped[dict | None] = mapped_column(JSONB)
    last_updated: Mapped[datetime] = mapped_column(
        SADateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_at: Mapped[datetime] = mapped_column(
        SADateTime(timezone=True), default=datetime.utcnow
    )


class TrialScore(Base):
    __tablename__ = "trial_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    trial_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    composite_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    composite_confidence: Mapped[float | None] = mapped_column(Numeric(5, 2))
    trial_promise_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    drug_profile_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    kol_sentiment_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    competitive_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    score_version: Mapped[str | None] = mapped_column(String(10))
    scored_at: Mapped[datetime] = mapped_column(
        SADateTime(timezone=True), default=datetime.utcnow
    )
