
from flask import render_template, redirect, url_for, request, abort, flash
import sqlalchemy as sa

from app import app, db




@app.route('/')
def index():
    books = db.session.scalars(sa.select(Book)).all()
    return render_template('index.html', books=books)