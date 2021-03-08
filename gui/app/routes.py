from flask import Flask
from flask import render_template, flash, redirect, request, url_for, session
from flask import send_file, send_from_directory, safe_join, abort
from app import app


@app.route('/')
def hello_world():
    return 'Hello, World!'
