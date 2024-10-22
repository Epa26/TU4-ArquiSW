from fastapi import APIRouter, HTTPException, Body
from app.models import GradeCreate
from app.services.mongodb import MongoDBService
from app.services.rabbitmq import Emit
from bson import ObjectId
from typing import Annotated
import logging

router = APIRouter()
mongo_service = MongoDBService()
emit_events = Emit()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
@router.post("/{course_id}/grades", summary='Registrar calificación')
async def register_grade(course_id: int, grade: Annotated[
                                                    GradeCreate,
                                                    Body(
                                                        examples=[
                                                            {
                                                                "student_id": 12,
                                                                "score": 96.5,
                                                                "parallel_id": 2
                                                            }
                                                        ],
                                                    )
                                                ]):
    """
    Registra una nueva calificación para un curso específico:

    - `course_id`: ID del curso

    Cuerpo

    - `student_id`: ID del estudiante
    - `score`: Nota del estudiante en el curso
    - `parallel_id`: ID del paralelo

    Además, se crea un evento a RabbitMQ indicando la creación de la calificación
    """
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

@router.get("/{course_id}/parallels/{parallel_id}/grades", summary='Listar calificaciones por paralelo')
async def list_grades(course_id: int, parallel_id: int, page: int = 1, limit: int = 10):
    """
    Lista todas las calificaciones asociadas a un curso y paralelo específico, con paginación:

    - `course_id`: ID del curso
    - `parallel_id`: ID del paralelo

    Parametros

    - `page`: Número de página (por defecto, 1)
    - `limit`: Cantidad de resultados por página (por defecto, 10)
    """
    grades = mongo_service.get_grades_by_parallel(course_id, parallel_id, page, limit)
    logging.info(f"Calificaciones listadas por course_id: {course_id} y parallel_id: {parallel_id}")
    for grade in grades:
        if isinstance(grade['_id'], ObjectId):
            grade['_id'] = str(grade['_id'])
    if not grades:
        raise HTTPException(status_code=404, detail="No grades found")
    return grades

# NUEVA RUTA: Consultar una calificación por ID
@router.get("/grades/{grade_id}", summary='Consultar calificación')
async def get_grade(grade_id: int):
    """
    Consulta los detalles de una calificación específica por su `grade_id`:

    - `grade_id`: ID de la calificación
    """
    grade = mongo_service.get_grade_by_id(grade_id)
    logging.info(f"Calificacion listada por grade_id: {grade_id}")
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    if isinstance(grade['_id'], ObjectId):
        grade['_id'] = str(grade['_id'])
    return grade

# NUEVA RUTA: Eliminar una calificación por ID
@router.delete("/grades/{grade_id}", summary='Eliminar una calificación')
async def delete_grade(grade_id: int):
    """
    Elimina una calificación específica por su `grade_id`:

    - `grade_id`: ID de la calificación

    Además, se crea un evento a RabbitMQ indicando la eliminación de la calificación
    """
    result = mongo_service.delete_grade_by_id(grade_id)
    logging.info(f"Calificacion eliminada por grade_id: {grade_id}")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Grade not found")
    emit_events.send(f"grade.{grade_id}.deleted", {"grade_id": grade_id})
    return {"message": "Grade deleted successfully"}


# Servicio para listar las calificaciones de un estudiante
@router.get("/{student_id}/grades", summary='Listar calificaciones del estudiante')
async def listar_calificaciones_estudiante(student_id: int,
    page: int = 1,
    limit: int = 10,
    min_score: int | None = None,
    max_score: int | None = None):
    """
    Lista todas las calificaciones asociadas al estudiante:

    - `student_id`: ID del estudiante
    
    Parametros

    - `page`: Número de página (por defecto, 1)
    - `limit`: Cantidad de resultados por página (por defecto, 10)
    - `min_score`(opcional): Filtro para definir una cota inferior de las calificaciones a buscar
    - `max_score`(opcional): Filtro para definir una cota superior de las calificaciones a buscar
    """
    skip = limit * (page - 1)
    grades = mongo_service.get_grades_by_student(student_id, page, limit)
    for grade in grades:
        if isinstance(grade['_id'], ObjectId):
            grade['_id'] = str(grade['_id'])
            
    # Aplicar filtros
    if min_score is not None:
        filtered_grades = []
        for grade in grades:
            if grade["score"] >= min_score:
                filtered_grades.append(grade)
        grades = filtered_grades

    if max_score is not None:
        filtered_grades = []
        for grade in grades:
            if grade["score"] <= max_score:
                filtered_grades.append(grade)
        grades = filtered_grades

    # Paginación
    paginated_grades = grades[skip: skip + limit]

    if not paginated_grades:
        raise HTTPException(status_code=404, detail="No se encontraron calificaciones")

    return paginated_grades

# Servicio para listar las calificaciones de un curso
@router.get("/{course_id}/grades", summary='Listar calificaciones de un curso')
async def listar_calificaciones_curso(course_id: int,
    page: int = 1,
    limit: int = 10,
    min_score: int | None = None,
    max_score: int | None = None):
    """
    Servicio para listar las calificaciones de un curso:

    - `course_id`: ID del curso
    
    Parametros

    - `page`: Número de página (por defecto, 1)
    - `limit`: Cantidad de resultados por página (por defecto, 10)
    - `min_score`(opcional): Filtro para definir una cota inferior de las calificaciones a buscar
    - `max_score`(opcional): Filtro para definir una cota superior de las calificaciones a buscar
    """
    skip = limit * (page - 1)
    grades = mongo_service.get_grades_by_course(course_id, page, limit)
    
    for grade in grades:
        if isinstance(grade['_id'], ObjectId):
            grade['_id'] = str(grade['_id'])

    # Aplicar filtros
    if min_score is not None:
        filtered_grades = []
        for grade in grades:
            if grade["score"] >= min_score:
                filtered_grades.append(grade)
        grades = filtered_grades

    if max_score is not None:
        filtered_grades = []
        for grade in grades:
            if grade["score"] <= max_score:
                filtered_grades.append(grade)
        grades = filtered_grades

    paginated_grades = grades[skip: skip + limit]

    if not paginated_grades:
        raise HTTPException(status_code=404, detail="No se encontraron calificaciones")

    return paginated_grades

# Servicio para actualizar una calificación existente
@router.put("/{course_id}/grades/{grade_id}", summary='Actualizar calificación')
async def actualizar_calificacion(course_id: int, grade_id: int, score: float):
    """
    Actualiza la calificación de un curso:

    - `course_id`: ID del estudiante
    - `grade_id`: ID del curso

    Parametros

    - `score`: Nueva calificación

    Además, se crea un evento a RabbitMQ indicando la actualización de la calificación
    """
    query_filter = {"course_id" : course_id,
                    "grade_id" : grade_id}
    update_operation = { '$set' : 
        { "score" : score }
    }
    result = mongo_service.update_grade(query_filter, update_operation)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Calificación o curso no encontrado")
    emit_events.send(f"grade.{grade_id}.updated", {"grade_id": grade_id, "course_id": course_id})
    return "Calificación actualizada exitosamente"