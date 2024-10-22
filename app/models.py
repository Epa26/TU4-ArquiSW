from pydantic import BaseModel

class Grade(BaseModel):
    grade_id: int
    student_id: int
    course_id: int
    score: float
    parallel_id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "grade_id": 1,
                    "student_id": 12,
                    "course_id": 365,
                    "score": 96.5,
                    "parallel_id": 2
                }
            ]
        }
    }

class GradeCreate(BaseModel):
    student_id: int
    score: float
    parallel_id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "student_id": 12,
                    "score": 96.5,
                    "parallel_id": 2
                }
            ]
        }
    }