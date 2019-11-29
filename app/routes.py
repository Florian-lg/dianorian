"""Import some useful modules"""
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy import desc
from app import app, db
from app.forms import AuthForm, RegisterForm, NewTweetForm, UpdateProfileForm
from app.models import User, Tweet

@app.route('/')
def home_redirection():
    """Redirection to avoid people on root"""
    return redirect(url_for('home'))

@app.route('/gaz', methods=['GET', 'POST'])
def home():
    """Home function, will render some tweets and forms"""
    form = NewTweetForm(prefix='user-')
    if form.validate_on_submit():
        if(len(form.text.data) <= 280):
            tweet = Tweet(message=form.text.data, user_id=current_user.id)
            db.session.add(tweet)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('Votre message est trop long...')
    tweets_list = Tweet.query.order_by(desc(Tweet.timestamp)).all()
    return render_template('home.html', form=form, tweets_list=tweets_list, user=current_user)

@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    """Show timeline"""
    tweets_list = Tweet.query.order_by(desc(Tweet.timestamp)).all()
    return render_template('tweet/timeline.html', tweets_list=tweets_list)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    """Authentification of users"""
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
    return render_template('user/forms/auth.html', form=form)

@app.route("/logout")
def logout():
    """Used to logout users"""
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Registration of users"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Feliciations, vous etes enregistre(e) !')
        return redirect(url_for('auth'))
    return render_template('user/forms/register.html', title='Register', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile"""
    if current_user.is_authenticated:
        return render_template('user/profile.html', user=current_user)
    return redirect(url_for('home'))

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """Edition form for user profile"""
    form = UpdateProfileForm()
    if current_user.is_authenticated:
        return render_template('user/editProfile.html', user=current_user, form=form)
    return redirect(url_for('home'))

@app.route('/timeline/<username>', methods=['GET', 'POST'])
def all_tweets_user(username):
    """Show all tweets for a specified user"""
    user = User.query.filter_by(username=username).first()
    tweets_list = Tweet.query.filter_by(user_id=user.id).all()
    return render_template('allTweetsUser.html', user=user, tweets_list=tweets_list)
