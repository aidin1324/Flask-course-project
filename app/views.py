import uuid

from app import app
from flask import render_template, request
from .db import stores, items
from flask_smorest import abort
@app.route('/')
def hello_world():
    return render_template('index.html')


