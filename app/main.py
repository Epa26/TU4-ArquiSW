from fastapi import FastAPI
from app.routes import grades
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

origin = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

app.include_router(grades.router, prefix="/api/v1")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

@app.get("/")
async def root():
    logging.info("👋 Hello world (end-point)!")
    return {"message": "Grade Management API is running!"}
