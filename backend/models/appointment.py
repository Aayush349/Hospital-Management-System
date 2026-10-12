from typing import Optional, Dict, Any
from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    id: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    patientName: Optional[str] = "Tushar Tawar"
    patientAge: Optional[int] = 32
    patientGender: Optional[str] = "Male"
    patientPhone: Optional[str] = "+91 98765 43210"
    doctorId: Optional[str] = None
    doctorName: Optional[str] = None
    department: Optional[str] = None
    doctorSpecialty: Optional[str] = None
    specialty: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = "10:00 AM"
    slot: Optional[str] = None
    timeSlot: Optional[str] = None
    status: Optional[str] = "Scheduled"
    tokenNumber: Optional[str] = None
    type: Optional[str] = "In-Person"
    symptoms: Optional[str] = ""
    historySummary: Optional[str] = ""
    vitals: Optional[Dict[str, Any]] = {}
    notes: Optional[str] = ""


class StatusUpdate(BaseModel):
    status: str
