from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List, Optional
from models.patient import PatientCreate, PatientUpdate
from services import patient_service

router = APIRouter(tags=["Patients"])


@router.get("/api/patients", response_model=List[Dict[str, Any]])
def get_all_patients():
    return patient_service.get_patients()


@router.post("/api/patients", status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate):
    return patient_service.add_patient(payload.dict())


@router.get("/api/patients/current")
def get_current_patient():
    pat = patient_service.get_patient("pat-1")
    if not pat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    return pat


@router.put("/api/patients/current")
def update_current_patient(payload: PatientUpdate):
    return patient_service.update_patient("pat-1", payload.dict(exclude_unset=True))


@router.get("/api/patient")
@router.get("/api/patient/{patient_id}")
def get_patient(patient_id: Optional[str] = "pat-1"):
    pat = patient_service.get_patient(patient_id or "pat-1")
    if not pat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return pat


@router.put("/api/patient")
@router.put("/api/patient/{patient_id}")
def update_patient(payload: PatientUpdate, patient_id: Optional[str] = "pat-1"):
    target_id = patient_id or "pat-1"
    return patient_service.update_patient(target_id, payload.dict(exclude_unset=True))


@router.delete("/api/patients/{patient_id}")
@router.delete("/api/patient/{patient_id}")
def delete_patient(patient_id: str):
    return patient_service.delete_patient(patient_id)
