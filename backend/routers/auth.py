from fastapi import APIRouter, HTTPException, status
from models.auth import LoginRequest, SignupRequest, ForgotPasswordRequest
from services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login")
def login(payload: LoginRequest):
    res = auth_service.login_user(payload.identifier, payload.password, payload.role)
    if not res.get("success"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.get("error"))
    return res


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest):
    if payload.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign up for Admin role is disabled for hospital cybersecurity compliance."
        )
    res = auth_service.register_user(payload.dict())
    if not res.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.get("error"))
    return res


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest):
    res = auth_service.reset_password(payload.identifier, payload.securityPin or "1234", payload.newPassword)
    if not res.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.get("error"))
    return res
