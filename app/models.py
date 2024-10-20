from pydantic import BaseModel
from bson import ObjectId

class Grade(BaseModel):
    id: int
    student_id: int
    course_id: int
    value: float
    parallel_id: int

    class Config:
        json_encoders = {ObjectId: str}

class GradeCreate(BaseModel):
    student_id: int
    value: float
    parallel_id: int
