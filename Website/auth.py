from flask import Blueprint,render_template
auth= Blueprint('auth',__name__)
@auth.route('/signup')
def signup():
    return render_template('signup.html')