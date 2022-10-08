from email import message
from flask import Flask, request,flash, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("create table if not exists user(pid integer primary key, username text, email text, rollnumber text, password text)")
con.close()

@app.route('/reg')
def reg():
    return render_template("register.html")

@app.route('/log')
def log():
    return render_template("login.html")


@app.route('/register', methods = ["POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            rollnumber = request.form["rollnumber"]
            password = request.form["password"]
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("insert into user(username, email, rollnumber, password)values(?,?,?,?)", (username, email, rollnumber, password))
            con.commit()
            msg = 'You have successfully registered !'
        except:
            msg = 'Error in registering'
        finally:
            con.close()
            return render_template("register.html", msg = msg)

@app.route('/login', methods = ["POST"])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from user where username=? and password=?", (username, password))
        data=cur.fetchone()

        if data:
            session['username']=data['username']
            session['rollnumber'] = data['rollnumber']
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect username/password !")
    return render_template('login.html')        
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('reg'))

if __name__ == '__main__':
    app.run(debug=True)