Documentación del Proyecto (Rama test)
1. Descripción General del Proyecto
Este proyecto implementa un sistema de gestión de calificaciones utilizando microservicios. El sistema incluye un servicio de almacenamiento y gestión de calificaciones en MongoDB, y un sistema de mensajería asíncrona con RabbitMQ para la transmisión de eventos relevantes al sistema.

2. Estructura del Proyecto
El proyecto sigue la siguiente estructura de directorios:
.
├── app/
│   ├── routes/
│   │   └── grades.py
│   ├── services/
│   │   ├── mongodb.py
│   │   └── rabbitmq.py
│   ├── main.py
│   └── models.py
├── assets/
├── Dockerfile
├── README.md
├── _app.py
├── data.py
├── docker-compose.yml
├── events.py
└── requirements.txt

app/routes/grades.py: Define las rutas relacionadas con la gestión de las calificaciones.
app/services/mongodb.py: Provee servicios de acceso y manipulación de datos en MongoDB.
app/services/rabbitmq.py: Maneja la mensajería asíncrona para la emisión de eventos usando RabbitMQ.
main.py: Define el punto de entrada principal para la API de FastAPI.
models.py: Define los modelos de datos para las calificaciones.

3. Funcionalidades Principales
3.1. Registrar una Calificación
Endpoint: POST /api/v1/{course_id}/grades
Descripción: Registra una nueva calificación para un curso específico.
Ejemplo de Petición:
{
  "student_id": 12345,
  "value": 90,
  "parallel_id": 1
}


3.2. Listar Calificaciones por Paralelo
Endpoint: GET /api/v1/{course_id}/parallels/{parallel_id}/grades
Descripción: Lista todas las calificaciones asociadas a un curso y paralelo específico, con paginación.
Parámetros:
page: Número de página (por defecto, 1).
limit: Cantidad de resultados por página (por defecto, 10).
3.3. Consultar una Calificación (Implementado)
Endpoint: GET /api/v1/grades/{grade_id}
Descripción: Consulta los detalles de una calificación específica por su grade_id.
Ejemplo de Respuesta:
{
  "grade_id": 1,
  "student_id": 12345,
  "course_id": 101,
  "value": 95,
  "parallel_id": 1
}

3.4. Eliminar una Calificación (Implementado)
Endpoint: DELETE /api/v1/grades/{grade_id}
Descripción: Elimina una calificación específica por su grade_id. Además, se envía un evento a RabbitMQ indicando la eliminación.
4. Servicios de MongoDB
Los servicios de MongoDB están implementados en app/services/mongodb.py y son los encargados de interactuar con la base de datos grade_management. Los métodos claves incluyen:

create_grade(grade_data): Crea una nueva calificación y la almacena en la base de datos.
get_grades_by_parallel(course_id, parallel_id, page, limit): Obtiene las calificaciones de un curso y paralelo específicos con paginación.
Métodos Añadidos:
get_grade_by_id(grade_id): Obtiene una calificación específica a través de su grade_id.
delete_grade_by_id(grade_id): Elimina una calificación específica a través de su grade_id.
5. Mensajería con RabbitMQ
El sistema utiliza RabbitMQ para manejar eventos asíncronos relacionados con la creación y eliminación de calificaciones. Estos eventos siguen un patrón de enrutamiento utilizando las claves grade.{grade_id}.created y grade.{grade_id}.deleted.

Exchange: grade_exchange
Tipo de Exchange: topic
Eventos emitidos:
Cuando se crea una nueva calificación: grade.{grade_id}.created.
Cuando se elimina una calificación: grade.{grade_id}.deleted.
6. Descripción de Archivos Clave
6.1. Dockerfile
Define la imagen de Docker que se utiliza para ejecutar la aplicación. Incluye la instalación de las dependencias necesarias.
FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

6.2. docker-compose.yml
Orquesta los servicios necesarios para levantar la aplicación, como MongoDB y RabbitMQ.
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongo
      - rabbitmq
    environment:
      - DATABASE_URL=mongodb://mongo:27017/grade_management

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

6.3. Events (events.py)
Se encarga de manejar los eventos de RabbitMQ tanto para la emisión como para la recepción de mensajes. Utiliza un exchange tipo topic para publicar eventos relacionados con las calificaciones.
import json
import pika
import logging

logging.getLogger("pika").setLevel(logging.ERROR)

host_name = 'localhost'

class Emit:
    def send(self, id, action, payload):
        self.connect()
        self.publish(id, action, payload)
        self.close()

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='grades',
                                      exchange_type='topic')

    def publish(self, id, action, payload):
        routing_key = f"grade.{id}.{action}"
        message = json.dumps(payload)

        self.channel.basic_publish(exchange='grades',
                                   routing_key=routing_key,
                                   body=message)

    def close(self):
        self.connection.close()

class Receive:
    def __init__(self):
        logging.info("Waiting for messages...")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name)
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='grades',
                                      exchange_type='topic')

        self.channel.queue_declare('grade_event_queue', exclusive=True)
        self.channel.queue_bind(exchange='grades', queue='grade_event_queue', routing_key="grade.*.*")
        self.channel.basic_consume(queue='grade_event_queue', on_message_callback=self.callback)

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        logging.info(f"Calificación del usuario modificada")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        self.connection.close()

6.4. Requisitos (requirements.txt)
Las dependencias necesarias para ejecutar el proyecto, incluyendo fastapi, pymongo, y pika para la integración con RabbitMQ.
fastapi
uvicorn
pymongo
pika

7. Cómo Ejecutar el Proyecto
7.1. Clonar el repositorio:
git clone -b test https://github.com/Epa26/TU4-ArquiSW.git

7.2. Levantar los contenedores con Docker:
docker-compose up --build

7.3. Acceder a la API:
Una vez que la aplicación esté corriendo, la API estará disponible en http://localhost:8000/api/v1.

Para verificar que el servicio esté funcionando correctamente, puedes acceder a la ruta principal GET /, que debería devolver un mensaje de estado.
