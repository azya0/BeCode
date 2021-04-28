from classes.courses import Courses
import json
import os


class Lesson:
    def __init__(self, name):
        self.name = name

    def get(self):
        return list(os.walk(f"courses/{self.name}"))[0][1]

    def list(self, lname):
        return list(os.walk(f"courses/{self.name}/{lname}"))[0][2]

    def len(self, lname):
        return len(list(os.walk(f"courses/{self.name}/{lname}"))[0][2])

    @staticmethod
    def passed_part(name, lesson, part, user_id):
        with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/{part}.json') as file:
            data = json.loads(file.read())
        return user_id in data['passed']
