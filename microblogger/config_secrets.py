import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

database = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}