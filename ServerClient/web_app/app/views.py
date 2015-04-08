import os
from flask import render_template, flash
from app import app
from app.user_files import UserFiles
from config import DOCS_DIR


@app.route('/')
@app.route('/index')
def index():
    users = os.listdir(DOCS_DIR)
    documents = []
    for user in users:
        documents.append({'username': user})

    return render_template("index.html",
                           title='Lista komputerów',
                           documents=documents)


@app.route('/<username>')
def user_files(username):
    user = None
    if os.path.isdir(os.path.join(DOCS_DIR, username)):
        user = UserFiles(username)
    else:
        flash('Folder komputera %s nie istnieje' % username)

    return render_template("user_document.html",
                           user=user,
                           title=username,
                           )