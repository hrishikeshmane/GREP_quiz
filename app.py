from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
#from flask_mysqldb import MySQL
#import MySQLdb.cursors



app = Flask(__name__)
app.secret_key = 'some secret key'

db = MySQLdb.connect(host="localhost" ,user="root" ,passwd="root", db='grep')
cursor = db.cursor()
#cursor.execute("SELECT * FROM login")
#numrows = cursor.rowcount

#for x in range(0, numrows):
#    row = cursor.fetchone()

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('welcome.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    u=request.form['username']
    querry="SELECT * FROM login where username='%s' " %(u,)
    cursor.execute(querry)
    row = cursor.fetchone()
    #print(row)
    if request.form['password'] == row[1]:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/reg')
def reg():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def do_register():
    u=request.form['username']
    p=request.form['password']
    querry="insert into login values('%s','%s') " %(u,p,)
    cursor.execute(querry)
    row1 = cursor.fetchone()
    db.commit()
    if row1==1:
        flash('registed')
    else:
        flash(' not registed')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/template')
def template():
    return render_template('first_page.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
