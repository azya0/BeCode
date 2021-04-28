import json
import flask
import sqlite3

cats_dict = {
    'topic_name': 'Welcome to Python',
    'name': 'What is Python?',
    'context': '''Синтаксис ядра языка минималистичен, за счёт чего на практике редко возникает необходимость обращаться к документации, сам же язык известен как интерпретируемый и используется в том числе для написания скриптов.
    ''',
    'type': 'question',
    'questions': 'Python - ... язык!',
    'answers': [
        'Компилируемый.',
        'Интерпритируемый.',
        'Флексовый.'
    ],
    'right_answer': 'Интерпритируемый.',
    'passed': [],
}

with open('courses/python/1. Welcome to Python/2.json', 'w') as cat_file:
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
cur.execute(f'''
                    UPDATE users
                    SET score = score + 1
                    WHERE id = 1
                    ''')

# con = sqlite3.connect("db/users.db")
# cur = con.cursor()
print(cur.execute(f'''Select score from users''').fetchall())