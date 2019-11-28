from flask import render_template, flash, redirect, url_for
from app import app, db
from datetime import datetime
from app.forms import AuthForm, RegisterForm, NewTweetForm, UpdateProfileForm
from flask_login import current_user, login_user
from app.models import User, Tweet
from sqlalchemy import desc

@app.route('/gaz', methods=['GET', 'POST'])
def home():
    form = NewTweetForm()
    if form.validate_on_submit():
        tweet = Tweet(message = form.message.data, user_id = current_user.id)
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('home'))
    tweets_list = Tweet.query.order_by(desc(Tweet.timestamp)).all()
    return render_template('home.html', form = form, tweets_list = tweets_list, user = current_user)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = AuthForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('user/forms/auth.html', form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, firstname = form.firstname.data, lastname = form.lastname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Feliciations, vous etes enregistre(e) !')
        return redirect(url_for('auth'))
    return render_template('user/forms/register.html', title='Register', form=form)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        return render_template('user/profile.html', user = current_user)
    else:
        return redirect(url_for('home'))

@app.route('/profile/edit', methods = ['GET', 'POST'])
def editProfile():
    form = UpdateProfileForm()
    if current_user.is_authenticated:
        return render_template('user/editProfile.html', user = current_user, form = form)
    else:
        return redirect(url_for('home'))