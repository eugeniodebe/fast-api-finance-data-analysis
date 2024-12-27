from fastapi import APIRouter, Depends, HTTPException, Header
from app.core.security.verify_secret import verify_secret

router = APIRouter()

# Open endpoint
@router.get("/open-hello")
def open_hello():
    return {"message": "Hello, Open World!"}

# Secured endpoint
@router.get("/secure-hello")
def secure_hello(x_secret_key: str = Depends(verify_secret)):
    return {"message": "Hello, Secure World!"}


