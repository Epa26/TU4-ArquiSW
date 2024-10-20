from fastapi import APIRouter, HTTPException
from app.models import GradeCreate
from app.services.mongodb import MongoDBService
from app.services.rabbitmq import Emit
from bson import ObjectId

router = APIRouter()
mongo_service = MongoDBService()
rabbitmq_service_emit = Emit()

@router.post("/{course_id}/grades")
async def register_grade(course_id: int, grade: GradeCreate):
    grade_data = grade.dict()
    grade_data["course_id"] = course_id
    result = mongo_service.create_grade(grade_data)
    
    if isinstance(result['_id'], ObjectId):
        result['_id'] = str(result['_id'])
    grade_data = {
        key: (str(value) if isinstance(value, ObjectId) else value) 
        for key, value in grade_data.items()
    }
    rabbitmq_service_emit.send(f"grade.{result['id']}.created", grade_data)
    return result

@router.get("/{course_id}/parallels/{parallel_id}/grades")
async def list_grades(course_id: int, parallel_id: int, page: int = 1, limit: int = 10):
    grades = mongo_service.get_grades_by_parallel(course_id, parallel_id, page, limit)
    for grade in grades:
        if isinstance(grade['_id'], ObjectId):
            grade['_id'] = str(grade['_id'])
    print(grades)
    if not grades:
        raise HTTPException(status_code=404, detail="No grades found")
    return grades
