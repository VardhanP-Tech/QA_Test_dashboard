from collections import Counter

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine, get_db
from .models import Defect, DefectStatus, Execution, TestCase, TestStatus
from .schemas import DefectCreate, DefectOut, ExecutionCreate, ExecutionOut, TestCaseCreate, TestCaseOut

Base.metadata.create_all(bind=engine)


def seed_demo_data():
    """Provide immediately useful data in an empty local/demo database."""
    db = SessionLocal()
    try:
        if db.scalar(select(TestCase.id).limit(1)):
            return
        cases = [
            TestCase(title="User can sign in with valid credentials", module="Authentication", priority="high", steps="Enter a valid email and password.", expected_result="Dashboard opens."),
            TestCase(title="Required fields are validated", module="Authentication", priority="medium", steps="Submit the sign-in form empty.", expected_result="Validation errors display."),
            TestCase(title="User can create a test case", module="Test management", priority="high", steps="Complete and submit the new test case form.", expected_result="Test case appears in the list."),
            TestCase(title="Defect can be reported from a failure", module="Defects", priority="medium", steps="Create a defect for a failed test.", expected_result="Defect is visible in the open queue."),
        ]
        db.add_all(cases)
        db.flush()
        db.add_all([
            Execution(test_case_id=cases[0].id, cycle="Regression v1.0", status=TestStatus.passed, executed_by="Asha Patel"),
            Execution(test_case_id=cases[1].id, cycle="Regression v1.0", status=TestStatus.failed, executed_by="Asha Patel", notes="Error message is not announced to screen readers."),
            Execution(test_case_id=cases[2].id, cycle="Regression v1.0", status=TestStatus.passed, executed_by="Rohan Shah"),
            Execution(test_case_id=cases[3].id, cycle="Regression v1.0", status=TestStatus.blocked, executed_by="Rohan Shah", notes="Defect service is unavailable."),
        ])
        db.add(Defect(title="Sign-in validation lacks accessible error announcement", severity="major", status=DefectStatus.open, test_case_id=cases[1].id, description="Screen reader users are not informed when validation fails."))
        db.commit()
    finally:
        db.close()


seed_demo_data()
app = FastAPI(title="QA Execution Dashboard API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/test-cases", response_model=list[TestCaseOut])
def list_test_cases(db: Session = Depends(get_db)):
    return db.scalars(select(TestCase).order_by(TestCase.created_at.desc())).all()


@app.post("/api/test-cases", response_model=TestCaseOut, status_code=201)
def create_test_case(payload: TestCaseCreate, db: Session = Depends(get_db)):
    item = TestCase(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item


@app.get("/api/executions", response_model=list[ExecutionOut])
def list_executions(db: Session = Depends(get_db)):
    return db.scalars(select(Execution).order_by(Execution.executed_at.desc())).all()


@app.post("/api/executions", response_model=ExecutionOut, status_code=201)
def create_execution(payload: ExecutionCreate, db: Session = Depends(get_db)):
    if not db.get(TestCase, payload.test_case_id):
        raise HTTPException(404, "Test case not found")
    item = Execution(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item


@app.get("/api/defects", response_model=list[DefectOut])
def list_defects(db: Session = Depends(get_db)):
    return db.scalars(select(Defect).order_by(Defect.created_at.desc())).all()


@app.post("/api/defects", response_model=DefectOut, status_code=201)
def create_defect(payload: DefectCreate, db: Session = Depends(get_db)):
    item = Defect(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item


@app.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    executions = db.scalars(select(Execution)).all()
    counts = Counter(item.status.value for item in executions)
    total = len(executions)
    return {
        "total_test_cases": len(db.scalars(select(TestCase)).all()),
        "total_executions": total,
        "pass_rate": round(counts["passed"] / total * 100, 1) if total else 0,
        "by_status": {status.value: counts[status.value] for status in TestStatus},
        "open_defects": len(db.scalars(select(Defect).where(Defect.status.in_(["open", "in_progress"]))).all()),
    }
