from fastapi import APIRouter, HTTPException
from app.models import GradeCreate
from app.services.mongodb import MongoDBService
from app.services.rabbitmq import Emit
from bson import ObjectId
import logging

router = APIRouter()
mongo_service = MongoDBService()
emit_events = Emit()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

@router.post("/{course_id}/grades")
async def register_grade(course_id: int, grade: GradeCreate):
    grade_id = mongo_service.get_next_sequence_value("grade_id")
    grade_data = grade.dict()
    grade_data["grade_id"] = grade_id
    grade_data["course_id"] = course_id
    result = mongo_service.create_grade(grade_data)
    logging.info(f"Calificacion registrada: {grade_data}")
    
    if isinstance(result['_id'], ObjectId):
        result['_id'] = str(result['_id'])
    grade_data = {
        key: (str(value) if isinstance(value, ObjectId) else value) 
        for key, value in grade_data.items()
    }
    emit_events.send(f"grade.{grade_id}.created", grade_data)
    return result

@router.get("/{course_id}/parallels/{parallel_id}/grades")
async def list_grades(course_id: int, parallel_id: int, page: int = 1, limit: int = 10):
    grades = mongo_service.get_grades_by_parallel(course_id, parallel_id, page, limit)
    logging.info(f"Calificaciones listadas por course_id: {course_id} y parallel_id: {parallel_id}")
    for grade in grades:
        if isinstance(grade['_id'], ObjectId):
            grade['_id'] = str(grade['_id'])
    if not grades:
        raise HTTPException(status_code=404, detail="No grades found")
    return grades

# NUEVA RUTA: Consultar una calificación por ID
@router.get("/grades/{grade_id}")
async def get_grade(grade_id: int):
    grade = mongo_service.get_grade_by_id(grade_id)
    logging.info(f"Calificacion listada por grade_id: {grade_id}")
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    if isinstance(grade['_id'], ObjectId):
        grade['_id'] = str(grade['_id'])
    return grade

# NUEVA RUTA: Eliminar una calificación por ID
@router.delete("/grades/{grade_id}")
async def delete_grade(grade_id: int):
    result = mongo_service.delete_grade_by_id(grade_id)
    logging.info(f"Calificacion eliminada por grade_id: {grade_id}")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Grade not found")
    emit_events.send(f"grade.{grade_id}.deleted", {"grade_id": grade_id})
    return {"message": "Grade deleted successfully"}
