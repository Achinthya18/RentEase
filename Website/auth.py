from flask import Blueprint, render_template,request,flash
import mysql.connector
try:
    conn=mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        port='3306'
    )
    if conn.is_connected():
        print("connected")
except:
    print("issues with connection")
cur=conn.cursor()
cur.execute("use test")
auth= Blueprint('auth',__name__)
@auth.route('/base')
def base():
    return render_template('base.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        address = request.form.get('address')
        phoneNumber = request.form.get('phoneNumber')
        password1 = request.form.get('password1')
        password2 = request.form.get('password')

        # Form Validation
        if len(email) < 4:
            flash('Email must have greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First Name must have greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must have greater than 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif not password1.isalnum():
            flash('Password must contain only alphanumeric characters.', category='error')
        elif not (phoneNumber.isdigit() and len(phoneNumber) != 10):
            flash('Phone Number must contain only digits.', category='error')
        else:
            # Input Sanitization and Database Operation
            try:
                cur.execute('''INSERT INTO Landlord
                                (LFname, LLname, LEmail, Lphone, LAddress, LPassword)
                                VALUES (%s, %s, %s, %s, %s, %s)''',
                            (firstName, lastName, email, phoneNumber, address, password1))
                conn.commit()
                flash('Account created successfully!', category='success')
            except Exception as e:
                flash(f'An error occurred: {str(e)}', category='error')
                conn.rollback()
    return render_template('signup.html')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    data=request.form
    print(data)
    email=request.form.get('email')
    
    paswd=request.form.get('password')
    
    return render_template('login.html')