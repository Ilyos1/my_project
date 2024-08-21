
from flask import render_template, redirect, url_for, request, abort, flash
import sqlalchemy as sa

from app import app, db




@app.route('/')
def index():
    tours = db.session.scalars(sa.select(Tour)).all()
    return render_template('index.html', tours=tours)