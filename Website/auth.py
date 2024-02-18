from flask import Blueprint, render_template,request,flash,redirect,session,url_for
import mysql.connector
try:
    conn=mysql.connector.connect(
        user='root',
        password='72aezakmi36',
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
<<<<<<< HEAD
=======
                print(properties[0])
>>>>>>> 33a54611bc30845133b67c38eb64cea31c3f770f
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
@auth.route('/propertyform', methods=['GET', 'POST'])
def propertyform():
    if request.method == 'POST':
        lid = session.get('lid')
        if lid:
            PCategory = request.form.get('PCategory')
            PLocation = request.form.get('PLocation')
            PCity = request.form.get('PCity')
            PState = request.form.get('PState')
            PPin = request.form.get('PPin')

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
    return render_template('propertyform.html')
@auth.route('/<int:pid>/tenantpage', methods=['GET', 'POST'])
def tenantpage(pid):
    session['pid'] = pid

    # Query the database to fetch tenant data based on pid
    cur.execute('''SELECT TFname, TLname, Rent, PaymentStatus, PayDate
                    FROM Tenant
                    JOIN Rent ON Tenant.Tid = Rent.Tid
                    WHERE Pid = %s''', (pid,))
    tenant_data = cur.fetchall()
    # Pass tenant data to the template for rendering
    return render_template('tenantpage.html', tenant_data=tenant_data)
@auth.route('/tenantform', methods=['GET', 'POST'])
def tenantform():
    if request.method == 'POST':
        pid = session['pid']  # Assuming you have a way to get the property ID
        TFname = request.form.get('TFname')
        TLname = request.form.get('TLname')
        TEmail = request.form.get('TEmail')
        TPhone = request.form.get('TPhone')
        DOC = request.form.get('DOC')

        Deposit = request.form.get('Deposit')
        Rent = request.form.get('Rent')
        PaymentStatus = request.form.get('PaymentStatus')
        PayDate = request.form.get('PayDate')

        try:
            # Insert Tenant details into the Tenant table
            cur.execute('''INSERT INTO Tenant
                            (TFname, TLname, TEmail, TPhone, DOC, Pid)
                            VALUES (%s, %s, %s, %s, %s, %s)''',
                        (TFname, TLname, TEmail, TPhone, DOC, pid))
            conn.commit()

            # Get the Tid of the newly inserted Tenant
            cur.execute('SELECT LAST_INSERT_ID()')
            tid = cur.fetchone()[0]

            # Insert Rental details into the Rent table
            cur.execute('''INSERT INTO Rent
                            (Lid, Tid, Deposit, Rent, PaymentStatus, PayDate)
                            VALUES (%s, %s, %s, %s, %s, %s)''',
                        (session.get('lid'), tid, Deposit, Rent, PaymentStatus, PayDate))
            conn.commit()

            flash('Tenant and Rental details added successfully!', category='success')
            return redirect(url_for('auth.tenantpage', pid=session['pid'])) # Redirect to home page after successful insertion
        except Exception as e:
            flash(f'An error occurred: {str(e)}', category='error')
            conn.rollback()

    return render_template('tenantform.html')



@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove the user's session data
    session.clear()
    # Redirect the user to the login page (or any other page you prefer)
    return redirect('/base')
