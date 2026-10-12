from fastapi import APIRouter, Header, status
from typing import Dict, Any, List, Optional
from models.prescription import PrescriptionCreate
from services import prescription_service

router = APIRouter(prefix="/api/prescriptions", tags=["Prescriptions"])


@router.get("", response_model=List[Dict[str, Any]])
def get_prescriptions(x_user_role: Optional[str] = Header(None, alias="X-User-Role")):
    role = x_user_role or "doctor"
    return prescription_service.get_prescriptions(role=role)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_prescription(payload: PrescriptionCreate):
    return prescription_service.create_prescription(payload.dict())


@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: str):
    return prescription_service.delete_prescription(prescription_id)
