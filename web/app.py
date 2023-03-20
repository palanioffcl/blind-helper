
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'mysecretkey'

con=sqlite3.connect("blind.db")


def is_authenticated():
    return 'username' in session

@app.route('/')
def home():
	return render_template("home.html")

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE name=? AND pass=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user is not None:
        session['username'] = user[1]
        return True
    else:
        return False


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fn = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        
        if password != confirm_password:
            return render_template('signup.html', message='Passwords do not match')
        else:
                with sqlite3.connect("blind.db") as con:
                        cur=con.cursor()
                        cur.execute("INSERT INTO users(name,mail,pass) VALUES (?,?,?,?)",(fn,email,generate_password_hash(password)))
                        con.commit()

        return redirect('/login')
    return render_template('signup.html')


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
	
    
        if user and check_password_hash({{row["pass"]}}, password):
            session['user'] = user
            return redirect('/dashboard')

      
        return render_template('login.html', message='Invalid email or password')
    return render_template('login.html')
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if authenticate(username, generate_password_hash(password)):
                return redirect('/dashboard')
            else:
                return render_template('login.html', error='Invalid username or password')
        else:
            return redirect('/dashboard')



@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    
    user = session['user']
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True)
