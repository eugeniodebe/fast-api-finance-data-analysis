from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os

# Use an environment variable for the secret key
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract the secret from headers (preferred) or query params
        secret = request.headers.get("X-Secret-Key") or request.query_params.get("secret")
        
        if secret != SECRET_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        # Proceed to the next middleware or endpoint
        response = await call_next(request)
        return response
