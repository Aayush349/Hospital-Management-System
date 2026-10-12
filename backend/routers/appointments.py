from fastapi import APIRouter, Header, status
from typing import Dict, Any, List, Optional
from models.appointment import AppointmentCreate, StatusUpdate
from services import appointment_service

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])


@router.get("", response_model=List[Dict[str, Any]])
def get_appointments(x_user_role: Optional[str] = Header(None, alias="X-User-Role")):
    role = x_user_role or "doctor"
    return appointment_service.get_appointments(role=role)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate):
    return appointment_service.create_appointment(payload.dict())


@router.patch("/{appointment_id}/status")
def update_status(appointment_id: str, payload: StatusUpdate):
    return appointment_service.update_appointment_status(appointment_id, payload.status)


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: str):
    return appointment_service.delete_appointment(appointment_id)
