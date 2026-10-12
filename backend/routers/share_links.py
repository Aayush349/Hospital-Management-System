from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List, Optional
from models.share_link import ShareLinkCreate, VerifyRequest
from services import share_link_service

router = APIRouter(prefix="/api/share-links", tags=["EHR Share Links"])


@router.get("", response_model=List[Dict[str, Any]])
def get_share_links(patientId: Optional[str] = "pat-1"):
    return share_link_service.get_share_links(patientId or "pat-1")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_share_link(payload: ShareLinkCreate):
    return share_link_service.create_share_link(payload.dict())


@router.delete("/{link_id}")
def delete_share_link(link_id: str):
    return share_link_service.delete_share_link(link_id)


@router.post("/verify")
def verify_share_link(payload: VerifyRequest):
    res = share_link_service.verify_share_link(payload.token, payload.password or "")
    if not res.get("success"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.get("error"))
    return res
