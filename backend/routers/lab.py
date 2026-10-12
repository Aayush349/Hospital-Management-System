from fastapi import APIRouter, Header, HTTPException, status
from typing import Optional
from models.lab import LabReportCreate, SampleOrderCreate, OrderStatusUpdate
from services import lab_service

router = APIRouter(tags=["Lab & Diagnostics"])


# Reports
@router.get("/api/lab/reports")
@router.get("/api/lab-reports")
def get_lab_reports(x_user_role: Optional[str] = Header(None, alias="X-User-Role")):
    role = x_user_role or "doctor"
    return lab_service.get_lab_reports(role=role)


@router.post("/api/lab-reports", status_code=status.HTTP_201_CREATED)
@router.post("/api/lab/reports", status_code=status.HTTP_201_CREATED)
def create_lab_report(payload: LabReportCreate):
    return lab_service.create_lab_report(payload.dict())


@router.delete("/api/lab/reports/{report_id}")
@router.delete("/api/lab-reports/{report_id}")
def delete_lab_report(report_id: str):
    return lab_service.delete_lab_report(report_id)


# Packages
@router.get("/api/lab/packages")
def get_lab_packages():
    return lab_service.get_lab_packages()


# Home sample tracker
@router.get("/api/lab/home-sample")
def get_home_sample_orders(patientId: Optional[str] = None):
    return lab_service.get_home_sample_orders(patientId)


@router.post("/api/lab/home-sample", status_code=status.HTTP_201_CREATED)
def book_home_sample(payload: SampleOrderCreate):
    return lab_service.create_home_sample_order(payload.dict())


@router.patch("/api/lab/orders/{order_id}/status")
def update_order_status(order_id: str, payload: OrderStatusUpdate):
    res = lab_service.update_sample_order_status(order_id, payload.status)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return res
