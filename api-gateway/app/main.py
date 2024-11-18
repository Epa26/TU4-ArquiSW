import logging
import requests

from ariadne import QueryType
from ariadne import MutationType
from ariadne import ObjectType
from ariadne import make_executable_schema
from ariadne import load_schema_from_path

from ariadne.asgi import GraphQL

from graphql.type import GraphQLResolveInfo

from starlette.middleware.cors import CORSMiddleware

type_defs = load_schema_from_path("./app/schema.graphql")

query = QueryType()
mutation = MutationType()

grade = ObjectType("Grade")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

api_url = "http://web:8000/api/v1"

@query.field("getGradeById")
def resolve_get_grade_by_id(obj, info: GraphQLResolveInfo, grade_id):
    response = requests.get(f"{api_url}/grades/{grade_id}")
    if response.status_code == 200:
        return response.json()

@query.field("getGradesByParallel")
def resolve_get_grades_by_parallel(obj, info: GraphQLResolveInfo, course_id, parallel_id):
    response = requests.get(f"{api_url}/{course_id}/parallels/{parallel_id}/grades")
    if response.status_code == 200:
        return response.json()

@query.field("getGradesByStudent")
def resolve_get_grades_by_student(obj, info: GraphQLResolveInfo, student_id):
    response = requests.get(f"{api_url}/students/{student_id}/grades")
    if response.status_code == 200:
        return response.json()
    
@query.field("getGradesByCourse")
def resolve_get_grades_by_student(obj, info: GraphQLResolveInfo, course_id):
    response = requests.get(f"{api_url}/{course_id}/grades")
    if response.status_code == 200:
        return response.json()

@mutation.field("registerGrade")
def resolve_register_grade(obj, info: GraphQLResolveInfo, course_id, student_id, score, parallel_id):
    payload = {
        "student_id": student_id,
        "score": score,
        "parallel_id": parallel_id
    }
    response = requests.post(f"{api_url}/{course_id}/grades", json=payload)
    if response.status_code == 200:
        return response.json()

@mutation.field("updateGrade")
def resolve_update_grade(obj, info: GraphQLResolveInfo, course_id, grade_id, score):
    payload = {"score": score}
    response = requests.put(f"{api_url}/{course_id}/grades/{grade_id}", json=payload)
    if response.status_code == 200:
        return response.json()

@mutation.field("deleteGrade")
def resolve_delete_grade(obj, info: GraphQLResolveInfo, grade_id):
    response = requests.delete(f"{api_url}/grades/{grade_id}")
    return response.status_code == 200


schema = make_executable_schema(type_defs, query, mutation, grade)
app = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=("GET", "POST", "OPTIONS", "PUT"))