from fastapi import FastAPI
from app.routes import grades
import logging

app = FastAPI()

app.include_router(grades.router, prefix="/api/v1")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

@app.get("/")
async def root():
    logging.info("👋 Hello world (end-point)!")
    return {"message": "Grade Management API is running!"}
