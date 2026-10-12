from typing import Optional, List
from pydantic import BaseModel


class ShareLinkCreate(BaseModel):
    id: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    token: Optional[str] = None
    title: Optional[str] = "Doctor Consultation Share Link"
    expiresAt: Optional[str] = None
    password: Optional[str] = None
    maxViews: Optional[int] = 5
    allowedSections: Optional[List[str]] = ['prescriptions', 'lab_reports', 'vitals', 'conditions']


class VerifyRequest(BaseModel):
    token: str
    password: Optional[str] = ""
