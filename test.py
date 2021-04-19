import json

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
    'right_answer': 'Язык программирования.'
}

with open('courses/python/1. Welcome to Python/1.json', 'w') as cat_file:
    json.dump(cats_dict, cat_file)