from pymongo import MongoClient

class MongoDBService:
    def __init__(self):
        self.client = MongoClient("mongodb://mongo:27017/")
        self.db = self.client.grade_management

    def create_grade(self, grade_data):
        self.db.grades.insert_one(grade_data)
        return grade_data

    def get_grades_by_parallel(self, course_id, parallel_id, page, limit):
        skips = limit * (page - 1)
        cursor = self.db.grades.find({"course_id": course_id, "parallel_id": parallel_id})
        grades = list(cursor.skip(skips).limit(limit))
        return grades

    def get_next_sequence_value(self, sequence_name: str) -> int:
        result = self.db.counters.find_one_and_update(
            {"_id": sequence_name},
            {"$inc": {"sequence_value": 1}},
            return_document=True
        )
        if not result:
            self.db.counters.insert_one({"_id": sequence_name, "sequence_value": 1})
            return 1
        return result["sequence_value"]

    # NUEVO MÉTODO: Consultar una calificación por ID
    def get_grade_by_id(self, grade_id: int):
        return self.db.grades.find_one({"grade_id": grade_id})

    # NUEVO MÉTODO: Eliminar una calificación por ID
    def delete_grade_by_id(self, grade_id: int):
        return self.db.grades.delete_one({"grade_id": grade_id})
