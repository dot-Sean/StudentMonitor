from flask import Flask

app = Flask(__name__)

from web_app.config import SECRET_KEY
app.secret_key = SECRET_KEY

from app import views