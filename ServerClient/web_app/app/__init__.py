from flask import Flask
from config import SECRET_KEY


app = Flask(__name__)

app.secret_key = SECRET_KEY

from app import views