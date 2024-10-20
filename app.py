from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import data 

app = FastAPI()

# Modelos
class Calificacion(BaseModel):
    id_estudiante: int
    id_curso: str
    calificacion: int

# Paginacion:
def paginar(items, skip: int = 0, limit: int = 10):
    return items[skip: skip + limit]

# Servicio para registrar una nueva calificación
@app.post("/calificaciones/estudiante/", response_model=Calificacion)
async def registrar_calificacion(calificacion: Calificacion):
    # Verificar si ya existe una calificación para ese estudiante en el curso
    for cal in data.calificaciones_simuladas:
        if cal["id_estudiante"] == calificacion.id_estudiante and cal["id_curso"] == calificacion.id_curso:
            raise HTTPException(status_code=400, detail="El estudiante ya tiene una calificación en este curso")

    # Agregar la nueva calificación
    nueva_calificacion = {
        "id_estudiante": calificacion.id_estudiante,
        "id_curso": calificacion.id_curso,
        "calificacion": calificacion.calificacion
    }
    data.calificaciones_simuladas.append(nueva_calificacion)

    return nueva_calificacion

# Servicio para actualizar una calificación existente
@app.put("/calificaciones/estudiante/", response_model=Calificacion)
async def actualizar_calificacion(calificacion: Calificacion):
    for cal in data.calificaciones_simuladas:
        if cal["id_estudiante"] == calificacion.id_estudiante and cal["id_curso"] == calificacion.id_curso:
            cal["calificacion"] = calificacion.calificacion
            return cal

    raise HTTPException(status_code=404, detail="Calificación no encontrada")


# Servicio para listar las calificaciones de un estudiante
@app.get("/calificaciones/estudiante/{id_estudiante}", response_model=List[Calificacion])
async def listar_calificaciones_estudiante(
    id_estudiante: int,
    skip: int = 0,
    limit: int = 10,
    min_calificacion: Optional[int] = Query(None),
    max_calificacion: Optional[int] = Query(None)
):
    calificaciones = []
    for cal in data.calificaciones_simuladas:
        if cal["id_estudiante"] == id_estudiante:
            calificaciones.append(cal)
    
    # Aplicar filtros
    if min_calificacion is not None:
        calificaciones_filtradas = []
        for cal in calificaciones:
            if cal["calificacion"] >= min_calificacion:
                calificaciones_filtradas.append(cal)
        calificaciones = calificaciones_filtradas

    if max_calificacion is not None:
        calificaciones_filtradas = []
        for cal in calificaciones:
            if cal["calificacion"] <= max_calificacion:
                calificaciones_filtradas.append(cal)
        calificaciones = calificaciones_filtradas

    # Paginacion
    calificaciones_paginadas = paginar(calificaciones, skip=skip, limit=limit)
    
    if not calificaciones_paginadas:
        raise HTTPException(status_code=404, detail="No se encontraron calificaciones")

    return calificaciones_paginadas

# Servicio para listar las calificaciones de un curso
@app.get("/calificaciones/curso/{id_curso}", response_model=List[Calificacion])
async def listar_calificaciones_curso(
    id_curso: str,
    skip: int = 0,
    limit: int = 10,
    min_calificacion: Optional[int] = Query(None),
    max_calificacion: Optional[int] = Query(None)
):
    calificaciones = [
        cal for cal in data.calificaciones_simuladas
        if cal["id_curso"] == id_curso
    ]
    
    # Aplicar filtros
    if min_calificacion is not None:
        calificaciones_filtradas = []
        for calificacion in calificaciones:
            if calificacion["calificacion"] >= min_calificacion:
                calificaciones_filtradas.append(calificacion)
        calificaciones = calificaciones_filtradas

    if max_calificacion is not None:
        calificaciones_filtradas = []
        for calificacion in calificaciones:
            if calificacion["calificacion"] <= max_calificacion:
                calificaciones_filtradas.append(calificacion)
        calificaciones = calificaciones_filtradas

    # Paginacion
    calificaciones_paginadas = paginar(calificaciones, skip=skip, limit=limit)
    
    if not calificaciones_paginadas:
        raise HTTPException(status_code=404, detail="No se encontraron calificaciones")

    return calificaciones_paginadas