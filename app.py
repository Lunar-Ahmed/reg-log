from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL-PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST' and 'id' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'address' in request.form and 'mobile' in request.form and 'age' in request.form and 'email' in request.form and 'password' in request.form:
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        mobile = request.form['mobile']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO register VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (id, firstname, lastname, address, mobile, age, email, password))        
        mysql.connection.commit()
        msg = 'Registration Successfully'
        return render_template('table.html')
    elif request.method == 'POST':
        msg = ''
    return render_template('index.html', msg=msg)


@app.route('/log', methods =['GET', 'POST'])
def log():
    if request.method == 'POST' and 'firstname' in request.form and 'email' in request.form and 'password' in request.form:
        firstname = request.form['firstname']
        email = request.form['email']
        password = request.form['passowrd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT* FROM register WHERE firstname = %s AND email = %s AND password= %s', (firstname, email, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session[firstname] = account['firstname']
            session['email'] = account['email']
            session['password'] = account['password']
            msg = 'Please fill form'
            return render_template('table.html', msg=msg)
        else:
            msg = 'please fill out form'
            return render_template('login.html', msg=msg)

if __name__ =='__main__':
    app.run(debug=True, port=5000)