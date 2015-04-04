from flask import Flask
from web_app.config import SECRET_KEY


app = Flask(__name__)

app.secret_key = SECRET_KEY

from web_app.app import views