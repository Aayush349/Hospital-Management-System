from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
from models.doctor import DoctorCreate, DoctorUpdate
from services import doctor_service

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])


@router.get("", response_model=List[Dict[str, Any]])
def get_doctors():
    return doctor_service.get_doctors()


@router.get("/{doctor_id}")
def get_doctor(doctor_id: str):
    doc = doctor_service.get_doctor_by_id(doctor_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return doc


@router.post("", status_code=status.HTTP_201_CREATED)
def add_doctor(payload: DoctorCreate):
    return doctor_service.add_doctor(payload.dict())


@router.put("/{doctor_id}")
def update_doctor(doctor_id: str, payload: DoctorUpdate):
    updated = doctor_service.update_doctor(doctor_id, payload.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return updated


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: str):
    return doctor_service.delete_doctor(doctor_id)
