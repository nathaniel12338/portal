from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL(app)
app = Flask(__name__, static_folder='static')


# Configure MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_DB'] = 'portal'

# Initialize MySQL extension
mysql.init_app(app)
# Sample username and password for demonstration purposes
valid_username = "florence@gmail.com"
valid_password = "password"

@app.route('/')
def index():
    # Retrieve the success message from the query string
    success_message = request.args.get('success_message', '')
    return render_template('index.html', success_message=success_message)

@app.route('/index', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the provided username and password match the valid credentials
        if username == valid_username and password == valid_password:
            # Authentication successful, redirect to Teacherpotel.html first
            return redirect(url_for('Teacherpotel', success_message='Successfully logged in'))
        else:
            # Authentication failed, show an error message
            error_message = "Invalid username or password. Please try again."
            return render_template('index.html', error_message=error_message)

@app.route('/Teacherpotel')
def Teacherpotel():
    # Retrieve the success message from the query string
    success_message = request.args.get('success_message', '')
    # Render Teacherpotel.html
    return render_template('Teacherpotel.html', success_message=success_message)



@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        # Get data from the form, including the logo filename
        school = request.form['schoolname']
        exam = request.form['examinationNo']
        first = request.form['firstname']
        last = request.form['lastname']
        date = request.form['date']
        gender = request.form['gender']
        classd = request.form['class']
        state = request.form['state']
        logo_filename = request.form['logo_filename']

        # Check if the user has uploaded a logo
        if not logo_filename:
            error_message = "Please upload a logo⚠️"
            return render_template('student.html', error_message=error_message)

        # Construct the URL for the logo using Flask's url_for
        logo_url = url_for('static', filename='imgs/' + logo_filename)

        # Check if the Examination No already exists in the database
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM sss WHERE examinationNo = %s", (exam,))
        result = cur.fetchone()
        cur.close()

        if result:
            # Examination No already exists, display a message
            error_message = "ExaminationNo already exists⚠️"
            return render_template('student.html', error_message=error_message)

        # Check if Examination No is exactly 5 numeric characters
        if not (exam.isalnum() and len(exam) == 5):
            # Display an error message
            error_message = "ExaminationNo should be exactly 5 characters⚠️"
            return render_template('student.html', error_message=error_message)

        # Examination No doesn't exist and meets the length requirement, proceed with form submission
        # Insert data into the database, including the logo filename
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO sss (schoolname, examinationNo, firstname, lastname, date, gender, class, state, logo_filename) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (school, exam, first, last, date, gender, classd, state, logo_url))
        mysql.get_db().commit()
        cur.close()

        # Optionally, you can redirect to a success page
        return redirect(url_for('Exampotal'))

    return render_template('student.html')

@app.route('/Exampotal', methods=['GET', 'POST'])
def Exampotal():
    if request.method == 'POST':
        # Get data from the form
        subject1 = request.form['subject1']
        grade1= request.form['grade1']
        subject2 = request.form['subject2']
        grade2 = request.form['grade2']
        subject3 = request.form['subject3']
        grade3 = request.form['grade3']
        subject4 = request.form['subject4']
        grade4 = request.form['grade4']
        subject5 = request.form['subject5']
        grade5 = request.form['grade5']
        subject6 = request.form['subject6']
        grade6 = request.form['grade6']
        subject7 = request.form['subject7']
        grade7 = request.form['grade7']
        subject8 = request.form['subject8']
        grade8 = request.form['grade8']
        subject9 = request.form['subject9']
        grade9 = request.form['grade9']
        subject10 = request.form['subject10']
        grade10 = request.form['grade10']
        print(subject1,grade1)
        cur = mysql.get_db().cursor()

        # Use placeholders in the query to avoid SQL injection
        query = "INSERT INTO exam (subject1,grade1,subject2,grade2,subject3,grade3,subject4,grade4,subject5,grade5,subject6,grade6,subject7,grade7,subject8,grade8,subject9,grade9,subject10,grade10) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (subject1,grade1,subject2,grade2,subject3,grade3,subject4,grade4,subject5,grade5,subject6,grade6,subject7,grade7,subject8,grade8,subject9,grade9,subject10,grade10)

        # Execute the query
        cur.execute(query, values)

        # Commit the changes to the database
        mysql.get_db().commit()

        # Close the cursor
        cur.close()

        # Redirect to a success page or do something else
        return render_template('Exampotal.html', success_message='Data submitted successfully', show_message_box=True)

    success_message = request.args.get('success_message', '')
    return render_template('Exampotal.html', success_message=success_message)


if __name__ == '__main__':
    app.run(debug=True)
