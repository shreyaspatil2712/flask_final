from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, db
from .forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd

# Create a blueprint
main = Blueprint('main', __name__)



@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, 'pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, 
                    password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route("/login", methods=["GET", "POST"])
def login():


    if current_user.is_authenticated:
        return redirect(url_for('dashboard1'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard1'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))


