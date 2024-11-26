from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

grade_id = 0

# Pruebas Endpoint POST "/{course_id}/grades"

## Test de registro de calificacion con campos válidos
def test_insert_grade_success():
    course_id = 1
    new_grade = {
        "student_id": 12,
        "score": 96,
        "parallel_id": 2
    }

    # Mock para funcion de envio de rabbitmq
    with patch('app.services.rabbitmq.Emit.send') as mock_send:
        response = client.post(f"/api/v1/{course_id}/grades", json=new_grade)
        
        assert response.status_code == 200
        response_data = response.json()

        assert response_data["student_id"] == new_grade["student_id"]
        assert response_data["score"] == new_grade["score"]
        assert response_data["parallel_id"] == new_grade["parallel_id"]
        assert response_data["course_id"] == course_id
        assert "grade_id" in response_data

        global grade_id
        grade_id = response_data["grade_id"]

        mock_send.assert_called_once()
    
## Test de registro de calificacion con campos inválidos, sin student_id y score mayor a 100
def test_insert_grade_failure():
    course_id = 1
    invalid_grade = {
        "score": 120,
        "parallel_id": 5
    }

    with patch('app.services.rabbitmq.Emit.send') as mock_send:
        response = client.post(f"/api/v1/{course_id}/grades", json=invalid_grade)
        
        assert response.status_code == 422

        mock_send.assert_not_called()

# Pruebas Endpoint GET "/grades/{grade_id}"

## Test de lectura de calificacion por id de calificacion
def test_read_grade():
    global grade_id
    response = client.get(f"/api/v1/grades/{grade_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, dict)

    assert "student_id" in response_data
    assert "score" in response_data
    assert "parallel_id" in response_data
    assert "course_id" in response_data
    assert response_data["grade_id"] == grade_id

## Test de lectura de calificacion por id de calificacion no encontrado
def test_read_grade_not_found():
    grade_id = -1
    response = client.get(f"/api/v1/grades/{grade_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "No se encontró calificación"}    

# Pruebas Endpoint GET "/students/{student_id}/grades"

## Test lectura de calificacion por id de estudiante
def test_read_grade_student():
    student_id = 12
    response = client.get(f"/api/v1/students/{student_id}/grades")
    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)

    for grade in response_data:
        assert "student_id" in grade
        assert "score" in grade
        assert "parallel_id" in grade
        assert isinstance(grade["score"], (int, float))
        assert 0 <= grade["score"] <= 100

## Test lectura de calificacion por id de estudiante no encontrado
def test_read_grade_student_not_found():
    student_id = -1
    response = client.get(f"/api/v1/students/{student_id}/grades")
    assert response.status_code == 404
    assert response.json() == {"detail": "No se encontraron calificaciones"}

# Pruebas Endpoint GET "/{course_id}/grades"

## Test lectura de calificacion por id de curso
def test_read_grade_course():
    course_id = 1
    response = client.get(f"/api/v1/{course_id}/grades")
    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)

    for grade in response_data:
        assert "student_id" in grade
        assert "score" in grade
        assert "parallel_id" in grade
        assert isinstance(grade["score"], (int, float))
        assert 0 <= grade["score"] <= 100

## Test lectura de calificacion por id de curso no encontrado
def test_read_grade_course_not_found():
    course_id = -1
    response = client.get(f"/api/v1/{course_id}/grades")
    assert response.status_code == 404
    assert response.json() == {"detail": "No se encontraron calificaciones"}

# Pruebas Endpoint GET "/{course_id}/parallels/{parallel_id}/grades"

## Test lectura de calificacion por id de curso e id de paralelo
def test_read_grade_course_parallel():
    course_id = 1
    parallel_id = 2
    response = client.get(f"/api/v1/{course_id}/parallels/{parallel_id}/grades")
    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)

    for grade in response_data:
        assert "student_id" in grade
        assert "score" in grade
        assert "parallel_id" in grade
        assert isinstance(grade["score"], (int, float))
        assert 0 <= grade["score"] <= 100

## Test lectura de calificacion por id de curso e id de paralelo no encontrados
def test_read_grade_course_parallel_not_found():
    course_id = -1
    parallel_id = -1
    response = client.get(f"/api/v1/{course_id}/parallels/{parallel_id}/grades")
    assert response.status_code == 404
    assert response.json() == {"detail": "No se encontraron calificaciones"}

# Pruebas Endpoint PUT "/{course_id}/grades/{grade_id}"

## Test actualización de calificacion por id de curso e id de calificacion
def test_update_grade():
    global grade_id
    course_id = 1
    score = 80

    with patch('app.services.rabbitmq.Emit.send') as mock_send:
        response = client.put(f"/api/v1/{course_id}/grades/{grade_id}?score={score}")
        assert response.status_code == 200
        assert response.json() == "Calificación actualizada exitosamente"

        mock_send.assert_called_once()

## Test actualización de calificacion por id de curso e id de calificacion no encontrado
def test_update_grade_failure():
    course_id = -1
    grade_id = -1
    score = -1

    with patch('app.services.rabbitmq.Emit.send') as mock_send:
        response = client.put(f"/api/v1/{course_id}/grades/{grade_id}?score={score}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Calificación o curso no encontrado"}

        mock_send.assert_not_called()

# Pruebas Endpoint DELETE "/grades/{grade_id}"

## Test eliminación de calificacion por id de calificacion
def test_delete_grade():
    global grade_id

    with patch('app.services.rabbitmq.Emit.send') as mock_send:
        response = client.delete(f"/api/v1/grades/{grade_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Calificación eliminada exitosamente"}

        mock_send.assert_called_once()

## Test eliminación de calificacion por id de calificacion no encontrado
def test_delete_grade_failure():
    grade_id = -1

    with patch('app.services.rabbitmq.Emit.send') as mock_send:
        response = client.delete(f"/api/v1/grades/{grade_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "No se encontró calificación"}

        mock_send.assert_not_called()
