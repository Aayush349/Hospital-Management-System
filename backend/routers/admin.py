from fastapi import APIRouter
from typing import Dict, Any, List
from services import admin_service, auth_service

router = APIRouter(tags=["Admin & Platform"])


@router.get("/api/admin/stats")
def get_admin_stats():
    return admin_service.get_admin_stats()


@router.get("/api/cloud/status")
def get_cloud_status():
    return admin_service.get_cloud_status()


@router.get("/api/users", response_model=List[Dict[str, Any]])
def get_users():
    return auth_service.get_users()
