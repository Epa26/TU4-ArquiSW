from fastapi import FastAPI
from app.routes import grades

app = FastAPI()

app.include_router(grades.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Grade Management API is running!"}
