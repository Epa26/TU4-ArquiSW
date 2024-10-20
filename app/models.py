from pydantic import BaseModel

class Grade(BaseModel):
    grade_id: int
    student_id: int
    course_id: int
    value: float
    parallel_id: int

class GradeCreate(BaseModel):
    student_id: int
    value: float
    parallel_id: int
