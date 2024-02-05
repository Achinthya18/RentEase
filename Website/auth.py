from flask import Blueprint, render_template,request,flash
auth= Blueprint('auth',__name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must have greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First Name must have greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must have greater than 7 characters.', category='error')
        elif password1 != password2:
            flash('Password does not match.', category='error')
        else:
            #add user to the database
            flash('Account created!', category='success')
    return render_template('signup.html')