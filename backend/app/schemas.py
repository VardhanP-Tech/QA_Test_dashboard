from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .models import DefectStatus, TestStatus


class TestCaseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    module: str
    priority: str = "medium"
    steps: str = ""
    expected_result: str = ""


class TestCaseOut(TestCaseCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ExecutionCreate(BaseModel):
    test_case_id: int
    cycle: str
    status: TestStatus
    executed_by: str
    notes: str = ""


class ExecutionOut(ExecutionCreate):
    id: int
    executed_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DefectCreate(BaseModel):
    title: str
    severity: str
    status: DefectStatus = DefectStatus.open
    test_case_id: int | None = None
    description: str = ""


class DefectOut(DefectCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
