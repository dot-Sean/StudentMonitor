import os


SECRET_KEY = 'some_secret_key'

APP_ROOT = os.path.abspath(os.path.dirname(__file__))

APP_STATIC = os.path.join(APP_ROOT, 'app', 'static')

DOCS_DIR = os.path.join(APP_STATIC, 'FILES')