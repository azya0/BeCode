import json
import flask
import sqlite3

cats_dict = {
    'topic_name': 'Welcome to Python',
    'name': 'What is Python?',
    'context': '''Рассмотрим функцию print(). В её скобках указывается аргумент, который будет выведен в консоль.
    ''',
    'type': 'label',
    'questions': 'What is output of this code?',
    'task': '''print(1)''',
    'right_answer': '1',
    'passed': [],
}

with open('courses/python/1. Welcome to Python/3.json', 'w') as cat_file:
    json.dump(cats_dict, cat_file)

# from classes.courses import Courses
# name = 'python'
# lesson = 1
#
#
# with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/1.json') as file:
#     data = json.loads(file.read())
#     print(data)
con = sqlite3.connect("db/users.db")
cur = con.cursor()

# con = sqlite3.connect("db/users.db")
# cur = con.cursor()
print(cur.execute(f'''Select * from users where login == "qwerty"''').fetchall())