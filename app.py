from flask import Flask, render_template, jsonify
from flask import request
from flask_security import current_user
from flask_login import LoginManager, login_required, current_user, UserMixin
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import yaml

app = Flask(__name__)


app.config['SECRET_KEY'] = 'Secret!'


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

bootstrap = Bootstrap(app)
mysql = MySQL(app)

class LoginForm(FlaskForm):
   username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
   password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
   remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
   email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
   username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
   password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
   
class EditForm(FlaskForm):
    address = StringField('address', validators=[InputRequired(), Length(min=2, max=80)])
    name = StringField('name', validators=[InputRequired(), Length(min=1, max=30)])
    remember = BooleanField('remember me')
    credit = StringField('credit', validators=[InputRequired(), Length(min=14, max=18)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	
   
@app.route("/")
@app.route("/home")
def index():
   return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
      cur = mysql.connection.cursor()
      cur.execute("select * from user where username=%s",[form.username.data])
      results = cur.fetchall()
      cur.close()
      print("RESULTS")
      print(results[0][2])
      if check_password_hash(results[0][2], form.password.data):
         return '<h1> right pass </h1>'
      else:
         return '<h1> wrong pass </h1>'
      
      return '<h1>' + form.username.data + ' ' + form.password.data +  ' ' + form.remember.data + '</h1>'

   return render_template('login.html', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
   form = RegisterForm()

      
   if form.validate_on_submit():
      cur = mysql.connection.cursor()
      hashedPassword = generate_password_hash(form.password.data, method='sha256')
      cur.execute("INSERT INTO user(username, email, password) VALUES(%s, %s, %s)",(form.username.data, form.email.data, hashedPassword))
      mysql.connection.commit()
      cur.close()
      return '<h1>' + form.email.data + ' ' + form.username.data + ' ' + form.password.data + '</h1>'
   
   return render_template('signup.html', form=form)

@app.route("/users")
def users():
   cur = mysql.connection.cursor()
   cur.execute("select * from user")
   userList = cur.fetchall()
   cur.close()
   return render_template('users.html', userList=userList)

@app.route("/books")
def books():
	return render_template('books.html')

@app.route("/construction")
def construction():
   return render_template('construction.html')

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    form = EditForm()
	
    print(form.validate_on_submit())
    if form.validate_on_submit():
      cur = mysql.connection.cursor()
      hashedPassword = generate_password_hash(form.password.data, method='sha256')
      cur.execute("select * from user where username=%s",[form.username.data])
      cur.execute("UPDATE user(address, password, name, credit) VALUES(%s, %s, %s, %s)",(form.address.data, hashedPassword, form.name.data, form.credit.data))
      results = cur.fetchall()
      print("RESULTS")
      print(results[0][2])
      if check_password_hash(results[0][2], form.password.data):
        print(address)
           # return edit_profile_2()
      else :
           print("wrong")
           return '<h1> wrong pass </h1>'
    return render_template('edit_profile.html', form=form)

@app.route("/return")
def returnBook():
   return render_template('return.html')

@app.route("/search")
def search():
   return render_template('search.html')

@app.route("/re_order")
def re_order():
   return render_template('re_order.html')
   
@app.route("/edit_profile_2", methods=['GET', 'POST'])
def edit_profile_2():
    form = EditForm()
	
    print(form.validate_on_submit())
    check1 = form.address.data
    check2 = form.name.data
    check3 = form.credit.data
    return '<h1>' + form.address.data
    if form.validate_on_submit():
      user.name = form.name.data
      user.credit = form.credit.data
      hashedPassword = generate_password_hash(form.password.data, method='sha256')
      user.password = hashedPassword
      mysql.connection.commit()
    elif request.method == 'GET':
      form.address.data = user.address
      form.name.data = user.name
      form.credit.data = user.credit
      return '<h1>' + form.address.data + ' ' + form.password.data + ' ' + form.name.data + form.credit.data + '</h1>'
    return render_template('edit_profile_2.html', form=form)

if __name__ == "__main__":
	app.run()