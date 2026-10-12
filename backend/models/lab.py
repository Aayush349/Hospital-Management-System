from typing import Optional
from pydantic import BaseModel


class LabReportCreate(BaseModel):
    id: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    testName: str
    testType: Optional[str] = "Biochemistry"
    department: Optional[str] = "Pathology Lab"
    date: Optional[str] = None
    doctorName: Optional[str] = "Pathologist"
    status: Optional[str] = "Completed"
    result: Optional[str] = ""
    normalRange: Optional[str] = ""
    unit: Optional[str] = ""
    summary: Optional[str] = ""
    fileName: Optional[str] = "Report.pdf"
    fileUrl: Optional[str] = "#"


class SampleOrderCreate(BaseModel):
    id: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    patientName: Optional[str] = "Tushar Tawar"
    testName: Optional[str] = "Full Body Checkup"
    date: Optional[str] = None
    timeSlot: Optional[str] = "08:00 AM - 09:00 AM"
    address: Optional[str] = "Home"
    phone: Optional[str] = "+91 98765 43210"
    fee: Optional[int] = 499


class OrderStatusUpdate(BaseModel):
    status: str
