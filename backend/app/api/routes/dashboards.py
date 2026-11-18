from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_employee, require_support
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import EmployeeDashboardOut, SupportDashboardOut
from app.services import dashboard_service

router = APIRouter(prefix="/api", tags=["dashboards"])


@router.get("/employee/dashboard", response_model=EmployeeDashboardOut)
def employee_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_employee),
) -> EmployeeDashboardOut:
    return dashboard_service.employee_dashboard(db, user)


@router.get("/support/dashboard", response_model=SupportDashboardOut)
def support_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_support),
) -> SupportDashboardOut:
    return dashboard_service.support_dashboard(db)
