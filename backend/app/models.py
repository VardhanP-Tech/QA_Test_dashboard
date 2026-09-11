from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class TestStatus(str, Enum):
    passed = "passed"
    failed = "failed"
    blocked = "blocked"
    not_run = "not_run"


class DefectStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class TestCase(Base):
    __tablename__ = "test_cases"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    module: Mapped[str] = mapped_column(String(100))
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    steps: Mapped[str] = mapped_column(Text, default="")
    expected_result: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Execution(Base):
    __tablename__ = "executions"
    id: Mapped[int] = mapped_column(primary_key=True)
    test_case_id: Mapped[int] = mapped_column(ForeignKey("test_cases.id"))
    cycle: Mapped[str] = mapped_column(String(100))
    status: Mapped[TestStatus] = mapped_column(SqlEnum(TestStatus), default=TestStatus.not_run)
    executed_by: Mapped[str] = mapped_column(String(100))
    notes: Mapped[str] = mapped_column(Text, default="")
    executed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Defect(Base):
    __tablename__ = "defects"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    severity: Mapped[str] = mapped_column(String(20))
    status: Mapped[DefectStatus] = mapped_column(SqlEnum(DefectStatus), default=DefectStatus.open)
    test_case_id: Mapped[int | None] = mapped_column(ForeignKey("test_cases.id"), nullable=True)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
