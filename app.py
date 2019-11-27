from flask import Flask, request, render_template, redirect, url_for
import csv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/user")
def user():
    return render_template('user/user.html')

@app.route("/auth")
def auth():
    return render_template('user/auth.html')

@app.route("/register")
def register():
    return render_template('user/register.html')