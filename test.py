import json
import flask
import sqlite3

cats_dict = {
    'topic_name': 'Welcome to Python',
    'name': 'What is Python?',
    'context': '''Python — высокоуровневый язык программирования, ориентированный на повышение производительности разработчика.
В наши дни Python является одним из наиболее востребованных языком на IT рынке.
    ''',
    'type': 'question',
    'questions': 'Python - это',
    'answers': [
        'Язык программирования.',
        'Змея.',
        'Я просто тестирую этот сайт, мне неинтересно.'
    ],
    'right_answer': 'Язык программирования.',
    'passed': [],
}

# with open('courses/python/1. Welcome to Python/task.json', 'w') as cat_file:
#     json.dump(cats_dict, cat_file)

# from classes.courses import Courses
# name = 'python'
# lesson = 1
#
#
# with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/task.json') as file:
#     data = json.loads(file.read())
#     print(data)
con = sqlite3.connect("db/users.db")
cur = con.cursor()
cur.execute(f'''
                    UPDATE users
                    SET score = score + 1
                    WHERE id = 1
                    ''')

# con = sqlite3.connect("db/users.db")
# cur = con.cursor()
print(cur.execute(f'''Select score from users''').fetchall())