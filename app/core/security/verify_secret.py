from fastapi import Header, HTTPException

SECRET_KEY = "your_secret_key_here"

async def verify_secret(x_secret_key: str = Header(None)):
    if x_secret_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")