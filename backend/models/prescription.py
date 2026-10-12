from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class PrescriptionCreate(BaseModel):
    id: Optional[str] = None
    appointmentId: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    patientName: Optional[str] = "Tushar Tawar"
    doctorId: Optional[str] = None
    doctorName: Optional[str] = None
    date: Optional[str] = None
    diagnosis: Optional[str] = None
    vitals: Optional[Dict[str, Any]] = {}
    medicines: Optional[List[Dict[str, Any]]] = []
    advice: Optional[str] = None
    followUp: Optional[str] = None
