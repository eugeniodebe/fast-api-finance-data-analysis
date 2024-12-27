from fastapi import FastAPI, Depends

from app.routers.hello import router as hello_router  # Import router properly
from app.routers.stock_overview import router as stocks_router
from app.routers.test_db import router as test_db_router
from app.core.security.verify_secret import verify_secret  # Import correctly
app = FastAPI()

# Include the Hello router
app.include_router(hello_router, prefix="/api/v1", tags=["hello"])


app.include_router(stocks_router, prefix="/api/v1", tags=["stocks"])


app.include_router(test_db_router, prefix="/api/v1", tags=["test-db"])



# # Secure route
# @app.get("/api/v1/secure-hello")
# async def secure_hello(x_secret_key: str = Depends(verify_secret)):
#     return {"message": "Hello, Secure World!"}

# # Open route
# @app.get("/api/v1/open-hello")
# async def open_hello():
#     return {"message": "Hello, Open World!"}
