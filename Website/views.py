from flask import Blueprint
views = Blueprint('views',__name__)

@views.route('/')
def home():
    return "<h1>home<h1>"