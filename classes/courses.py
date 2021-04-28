import os


class Courses:
    def __init__(self):
        self.courses = list(os.walk("courses"))[0][1]

    def get(self):
        return sorted(list(map(lambda x: x.capitalize(), self.courses)))

    @staticmethod
    def len_of_course(name_of_course):
        return len(list(os.walk(f"courses/{name_of_course.lower()}"))[0][2])

    def course_data(self, name_of_course):
        return {
            'name': name_of_course.capitalize(),
            'lessons': self.len_of_course(name_of_course)
        }

    @staticmethod
    def get_list_of_courses(name_of_course):
        return list(os.walk(f"courses/{name_of_course.lower()}"))[0][1]
