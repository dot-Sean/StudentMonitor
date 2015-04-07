import os
from flask import render_template, flash
from app import app
from app.user_files import UserFiles
from config import DOCS_DIR


@app.route('/')
@app.route('/index')
def index():
    documents = [
        {'username': 'BURCHARDTIST-PC'},
        {'username': 'aśka'},
        {'username': 'krzysiek'}
    ]

    return render_template("index.html",
                           title='Lista komputerów',
                           documents=documents)


@app.route('/<username>')
def user_files(username):
    user_files = UserFiles(username)
    if not user_files:
        flash('Dokument komputera %s nie istnieje' % username)

    return render_template("user_document.html",
                           user_files=user_files,
                           ss_dir=os.path.join(DOCS_DIR, username),
                           title=username
                           )