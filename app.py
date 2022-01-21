from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from sqlalchemy.sql.expression import null
from flask import Flask,request,render_template,session,redirect,url_for

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

#create database for individual values


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
                return redirect(url_for('home_employee', username=duname))
                #return render_template('home_employee.html')
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
        return render_template('login.html')

@app.route('/home_employee')
def home_employee():
    unm = request.args.get('username', None)
    finalunm = unm.split('_')
    return render_template('home_employee.html', username=finalunm[0])    

#question
@app.route('/question')
def question():
    return render_template('questionnaire.html')

@app.route('/out')
def out():
    return render_template('login.html')

@app.route('/stress')
def stress():
    return render_template('home_employee.html')

@app.route('/factor')
def factor():
    return render_template('factor_analysis.html')

#setting debug true makes server auto restart if any changes in code are detected
if __name__ == '__main__':
    app.run(debug=True)