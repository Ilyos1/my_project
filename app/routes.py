import os

from flask import render_template, redirect, url_for, request, abort, flash, send_from_directory
import sqlalchemy as sa
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import LoginForm, RegistrationForm, BookForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import Book, User
from app.send_mail import send_reset_password_email, send_confirmation_email


@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
# @admin_required
def edit_book(book_id):
    book = db.session.scalar(sa.select(Book).where(Book.id == book_id))
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.name = form.name.data
        book.description = form.description.data
        book.country = form.country.data
        book.price = form.price.data
        book.author = form.author.data
        book.year = form.year.data
        db.session.commit()

        flash('You successfully edited a book', category='success')
        return redirect(url_for('index'))
    return render_template('edit_book.html', form=form)


@app.route('/')
def index():
    books = db.session.scalars(sa.select(Book)).all()
    return render_template('index.html', books=books)


@app.route('/profile')
def profile():
    user_books = db.session.scalars(current_user.user_books.select())
    return render_template('profile.html', user_books=user_books)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # send_confirmation_email(user)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/book/new', methods=['GET', 'POST'])
# @admin_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(name=form.name.data, description=form.description.data,
                    country=form.country.data, price=form.price.data, author=form.author.data,
                    year=form.year.data)

        uploaded_file = form.photo.data
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            photo_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            uploaded_file.save(photo_path)
            relative_photo_path = os.path.join('uploads', filename).replace('\\', '/')
            book.photo = relative_photo_path

        uploaded_txt = form.book_txt.data
        if uploaded_txt:
            txt_filename = secure_filename(uploaded_txt.filename)
            read_path = os.path.join(app.config['READ_PATH'], txt_filename)
            uploaded_txt.save(read_path)
            relative_txt_path = os.path.join('read', txt_filename).replace('\\', '/')
            book.book_txt = relative_txt_path

        selected_genres = []
        if form.Fiction.data:
            selected_genres.append('Fiction')
        if form.Romance.data:
            selected_genres.append('Romance')
        if form.Mystery.data:
            selected_genres.append('Mystery')
        if form.Fantasy.data:
            selected_genres.append('Fantasy')
        if form.Horror.data:
            selected_genres.append('Horror')
        if form.Biography.data:
            selected_genres.append('Biography')
        if form.Comedy.data:
            selected_genres.append('Comedy')
        book.genres = ', '.join(selected_genres)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_book.html', form=form)


@app.route('/book/save/<int:book_id>')
def save_book(book_id):
    book = db.session.scalar(sa.select(Book).where(Book.id == book_id))
    user_books = db.session.scalars(current_user.user_books.select())
    if book in user_books:
        return '<h1>You have already saved this book</h1>'
    current_user.user_books.add(book)
    db.session.commit()
    return '<h1>You have saved this book successfully</h1>'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data) or not user.is_active:
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/confirm-email/<token>')
def confirm_email(token):
    user = User.verify_token(token)  # USER or None
    if not user:
        return '<h1>Cannot confirm your email</h1>'
    user.is_active = True
    db.session.commit()
    return '<h1>You have confirmed your email successfully</h1>'


@app.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_reset_password_email(user)
    return render_template('reset_password_request.html', form=form)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token(token)  # USER or None
    if not user:
        return '<h1>Invalid link</h1>'
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/read/book/<path:filename>')
def read_book(filename):
    return send_from_directory('static', filename)
