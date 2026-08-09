from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.property import Property, Unit, UnitStatus
from app.models.application import RentalApplication
from app.models.maintenance import MaintenanceRequest
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_org_id, require_roles
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports & Analytics"])

@router.get("/dashboard-analytics", response_model=APIResponse[Dict[str, Any]])
def get_dashboard_analytics(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    total_properties = db.query(Property).filter(Property.organization_id == org_id, Property.is_deleted == False).count()
    units = db.query(Unit).filter(Unit.organization_id == org_id, Unit.is_deleted == False).all()
    total_units = len(units)
    occupied_units = sum(1 for u in units if u.status == UnitStatus.OCCUPIED)
    vacant_units = sum(1 for u in units if u.status == UnitStatus.AVAILABLE)
    
    pending_apps = db.query(RentalApplication).filter(RentalApplication.organization_id == org_id, RentalApplication.status == "SUBMITTED").count()
    open_maintenance = db.query(MaintenanceRequest).filter(MaintenanceRequest.organization_id == org_id, MaintenanceRequest.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"])).count()

    monthly_revenue = [18500, 19200, 21000, 20500, 22400, 24800]
    monthly_expenses = [4200, 3800, 5100, 4600, 3900, 4800]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    return APIResponse(
        success=True,
        data={
            "total_properties": total_properties,
            "total_units": total_units,
            "occupied_units": occupied_units,
            "vacant_units": vacant_units,
            "occupancy_rate": round((occupied_units / total_units * 100), 1) if total_units > 0 else 0.0,
            "pending_applications": pending_apps,
            "open_maintenance": open_maintenance,
            "revenue_chart": {"labels": months, "revenue": monthly_revenue, "expenses": monthly_expenses}
        }
    )
