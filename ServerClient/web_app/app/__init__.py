from flask import Flask

app = Flask(__name__)
app.secret_key = 'some_secret_key'

from web_app.app import views