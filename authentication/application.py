from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler

@application.route("/login") 
def login():
    return render_template("login.html")




