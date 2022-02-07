from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from sqlalchemy.sql.expression import null
from flask import Flask,request,render_template,session,redirect,url_for
from threading import Thread
from detect_blinks import return_array_eye_blinks, start_eye_blink_count
import json
#-----------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DetectionDatabase.db'
db = SQLAlchemy(app)
#-----------------------------------------------------------------------------------------------------------------
#create_database having table User with 3 columns
class User(db.Model):
    emp_index = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, unique=True)
    emp_name = db.Column(db.String(20), nullable=False)
    emp_mobile = db.Column(db.String(10), nullable=False)
    emp_addr = db.Column(db.String(100), nullable=False)
    emp_dept = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.username}')"

db.create_all()

#-----------------------------------------------------------------------------------------------------------------

#add individual values in db here


@app.route('/')
def hello_world():
    return render_template("login.html")

#-----------------------------------------------------------------------------------------------------------------

@app.route('/form_login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        duname=request.form['username']
        dpass=request.form['password']
        user = User.query.filter_by(username=duname).first()
        if user:
            passchk = User.query.filter_by(username=duname , password=dpass).first()
            if passchk:
                session['username'] = duname
                s = session['username']
                thr = Thread(target=start_eye_blink_count, args=[])
                thr.start()
                return redirect(url_for('home_employee', username=s))
            else:
                return render_template('login.html')
        else:
            if duname=='admin':
                if dpass=='Mk$as%k12pasO':
                    return render_template('home_admin.html')
                else:
                    return render_template('login.html')
            else:
                return render_template('login.html')

@app.route('/home_employee')
def home_employee():
    if('username' in session):
        unm = session['username']
        finalunm = unm.split('_') 
        return render_template('home_employee.html', username=finalunm[0])  
    else:
        return render_template('login.html')

#question
@app.route('/question')
def question():
    if('username' in session):
        unm = session['username']
        finalunm = unm.split('_') 
        return render_template('questionnaire.html',username=finalunm[0])
    else:
        return render_template('login.html')

@app.route('/stress')
def stress():
    if('username' in session):
        unm = session['username']
        finalunm = unm.split('_') 
        return render_template('home_employee.html',username=finalunm[0])
    else:
        return render_template('login.html')

@app.route('/factor')
def factor():
    if('username' in session):
        unm = session['username']
        finalunm = unm.split('_') 
        arr = return_array_eye_blinks()
        return render_template('factor_analysis.html',username=finalunm[0],eye_blink_arr=json.dumps(arr))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        session.pop('username')         
        return redirect('/')
    except:
        return render_template('login.html')

#setting debug true makes server auto restart if any changes in code are detected
if __name__ == '__main__':
    app.run(debug=True)