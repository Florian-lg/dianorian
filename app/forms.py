""""Import some useful modules"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_login import current_user
from app.models import User

class AuthForm(FlaskForm):
    """Authentification form"""
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

class RegisterForm(FlaskForm):
    """Registration form"""
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetez le mot de passe', validators=[DataRequired(), EqualTo('password')])
    firstname = StringField('Prenom', validators=[DataRequired()])
    lastname = StringField('Nom', validators=[DataRequired()])
    submit = SubmitField('S\'enregistrer')

    def validate_username(self, username):
        """user validation"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Email validation"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NewTweetForm(FlaskForm):
    """New Tweet form"""
    name = StringField('Votre nom : ', validators=[DataRequired()])
    text = StringField('Entrez votre tweet', validators=[DataRequired()])
    submit = SubmitField('Pyttez !')

class UpdateProfileForm(FlaskForm):
    """Profile update form"""
    #get user
    user = current_user
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetez le mot de passe', validators=[DataRequired(), EqualTo('password')])
    firstname = StringField('Prenom', validators=[DataRequired()], default="prenom")
    lastname = StringField('Nom', validators=[DataRequired()], default="nom")
    submit = SubmitField('Enregistrer')
