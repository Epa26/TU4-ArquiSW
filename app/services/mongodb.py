from pymongo import MongoClient

class MongoDBService:
    def __init__(self):
        self.client = MongoClient("mongodb://mongo:27017/")
        self.db = self.client.grade_management

    def create_grade(self, grade_data):
        result = self.db.grades.insert_one(grade_data)
        return {"id": str(result.inserted_id), **grade_data}

    def get_grades_by_parallel(self, course_id, parallel_id, page, limit):
        skips = limit * (page - 1)
        cursor = self.db.grades.find({"course_id": course_id, "parallel_id": parallel_id})
        grades = list(cursor.skip(skips).limit(limit))
        return grades
