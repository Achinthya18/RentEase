from flask import Blueprint, render_template,request,flash,redirect,session
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
cur.execute("use rentalManagement")
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
        elif not (phoneNumber.isdigit() ):
            flash('Phone Number must contain only digits.', category='error')
        else:
            # Input Sanitization and Database Operation
            try:
                cur.execute('''INSERT INTO Landlord
                                (LFname, LLname, LEmail, Lphone, LAddress, LPassword)
                                VALUES (%s, %s, %s, %s, %s, %s)''',
                            (firstName, lastName, email, phoneNumber, address, password1))
                conn.commit()
                cur.execute("SELECT LAST_INSERT_ID();")
                lid = cur.fetchone()[0]
                session['lid'] = lid
                flash('Account created successfully!', category='success')
                
                
            except Exception as e:
                flash(f'An error occurred: {str(e)}', category='error')
                conn.rollback()
    return render_template('signup.html')
@auth.route('/home', methods=['GET', 'POST'])
def home():
    # Retrieve the landlord ID from the session
    lid = session.get('lid')
    if lid:
            # Fetch all properties associated with the current landlord
            cur.execute('''SELECT *
                            FROM Property
                            WHERE Lid = %s''', (lid,))
            properties = cur.fetchall()
            if properties:
                print(properties[0])
            # Pass the fetched properties to the template for rendering
                return render_template('home.html', properties=properties)
    else:
        flash('Landlord ID not found in session.', category='error')
    return render_template('home.html')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') 
        paswd = request.form.get('password')
        sql = '''
                SELECT Lid, LPassword
                FROM Landlord
                WHERE LEmail = %s
            '''
        try:
            cur.execute(sql, (email,))
            data = cur.fetchone()
            if data:
                lid, stored_password = data  # Fetch Lid and stored password from database
                if stored_password == paswd:
                    session['lid'] = lid  # Store Lid in session
                    return redirect('/home')
                else:
                    flash('The entered password is incorrect', category='error')                 
            else:
                flash('The email id doesn\'t exist', category='error')
        except Exception as e:
            flash(str(e), category='error')
    return render_template('login.html')
@auth.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
@auth.route('/tenantform', methods=['GET', 'POST'])
def tenantform():
    if request.method == 'POST':
        lid = session.get('lid')
        if lid:
            PCategory = request.form.get('PCategory')
            PLocation = request.form.get('PLocation')
            PCity = request.form.get('PCity')
            PState = request.form.get('PState')
            PPin = request.form.get('PPin')
            print("PCategory:", PCategory)
            print("PLocation:", PLocation)

            try:
                # Insert property details into the Property table
                cur.execute('''INSERT INTO Property
                                (Lid, PCategory, PLocation, PCity, PState, PPin)
                                VALUES (%s, %s, %s, %s, %s, %s)''',
                            (lid, PCategory, PLocation, PCity, PState, PPin))
                conn.commit()
                
                flash('Property details added successfully!', category='success')
                return redirect('/home')  # Redirect to home page after successful insertion
            except Exception as e:
                flash(f'An error occurred: {str(e)}', category='error')
                conn.rollback()
        else:
            flash('Landlord ID not found in session.', category='error')

    return render_template('tenantform.html')
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove the user's session data
    session.clear()
    # Redirect the user to the login page (or any other page you prefer)
    return redirect('/base')