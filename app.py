from flask import Flask, render_template, jsonify, url_for, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import yaml

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Secret!'
app.config.from_pyfile('config.cfg')

loggedIn = False
username = None

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

bootstrap = Bootstrap(app)
mysql = MySQL(app)

class LoginForm(FlaskForm):
   username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
   password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
   remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
   email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
   name = StringField('full name', validators=[InputRequired(), Length(min=1, max=100)])
   username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
   phone = StringField('phone number', validators=[InputRequired(), Length(min=7, max=15)])
   password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
   ccnumber = StringField('credit card number', validators=[InputRequired(), Length(min=14, max=18)])
   address = StringField('address', validators=[InputRequired(), Length(min=2, max=80)])

class EditForm(FlaskForm):
   address = StringField('address', validators=[Length(min=2, max=80)])
   name = StringField('full name', validators=[Length(min=1, max=100)])
   ccnumber = StringField('credit card number', validators=[Length(min=14, max=18)])
   currpassword = PasswordField('current password', validators=[Length(min=8, max=80)])
   newpassword = PasswordField('new password', validators=[Length(min=8, max=80)])

class ForgotPass(FlaskForm):
   username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
   email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

class ChangePass(FlaskForm):
   username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
   newpassword = PasswordField('new password', validators=[Length(min=8, max=80)])

class User():
   username =""
   address = ""
   cc = ""
   email = ""
   def __init__(self, username):
      self.username = username
      cur = mysql.connection.cursor()
      rowcount = cur.execute("select * from user where username=%s", [self.username])
      results = cur.fetchall()
      cur.close()
      print("IN USER")
      print(results[0][2]) #PASSWORD
      print(results[0][3]) #EMAIL
      print(results[0][5]) #CC NUMBER
      print(results[0][6]) #ADDRESS
      print(results[0][7]) # NAME
      print(results[0][7]) #PHONE
      print(results[0][7])

      # This is where we would get the remaining feilds from the database
      # And set the corresponding values so that we can acsess them from the html file

      
      
      

@app.route("/")
@app.route("/home")
def home():
   print(loggedIn)
   print(username)
   return render_template('index.html')

@app.route("/logout")
def logout():
   session['user'] = None
   session['loggedIn'] = False
   
   return redirect(url_for('home'))

@app.route("/login", methods=['GET', 'POST'])
def login():
   form = LoginForm()

   if form.validate_on_submit():
      cur = mysql.connection.cursor()
      rowcount = cur.execute("select * from user where username=%s",[form.username.data])
      results = cur.fetchall()
      cur.close()
      print("RESULTS")
      if rowcount > 0:
         print(results[0][2])
         if(results[0][4]==1):
            if check_password_hash(results[0][2], form.password.data):
               session['user'] = form.username.data
               session['loggedIn'] = True
               user = User(form.username.data)
               if results[0][9]==1:
                  session['isAdmin'] = True
               else:
                  session['isAdmin'] = False
               return redirect(url_for('home'))
            else:
               return render_template('login.html', form=form, incorrectPass=True)
         else:
            return '<h1>account has not been verified.<h1>'
      else:
         return render_template('login.html', form=form, incorrectUser=True)
   return render_template('login.html', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
   form = RegisterForm()

      
   if form.validate_on_submit():
      cur = mysql.connection.cursor()
      hashedPassword = generate_password_hash(form.password.data, method='sha256')
      cur.execute("INSERT INTO user(username, email, password, phone, address, name) VALUES(%s, %s, %s, %s, %s, %s)",(form.username.data, form.email.data, hashedPassword, form.phone.data, form.address.data, form.name.data))
      mysql.connection.commit()
      cur.close()

      token = s.dumps(form.email.data, salt='email-confirm')

      print("TOKENTOKEN " + token)
      msg = Message('Confirm Email', sender="ugaonlinebookstore@gmail.com", recipients=[form.email.data])

      link = url_for('confirm_email', token=token, _external=True)

      msg.body = 'Your confirmation link is {}'.format(link)

      mail.send(msg)

      return '<h1>check for confirmation email at ' + form.email.data + '</h1>'
   
   return render_template('signup.html', form=form)

@app.route("/confirm_email/<token>")
def confirm_email(token):
   email = s.loads(token, salt='email-confirm', max_age=120)
   print(email)
   cur = mysql.connection.cursor()
   cur.execute("UPDATE user SET verified=1 where email like %s",[email])
   mysql.connection.commit()
   cur.close()
   return '<h1>your account with email ' + email + ' has been confirmed!</h1>'


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

   if form.validate_on_submit():
      cur = mysql.connection.cursor()
      hashedPassword = generate_password_hash(form.newpassword.data, method='sha256')
      cur.execute("""
         UPDATE user
         SET address=%s, name=%s, ccnumber=%s, password=%s
         WHERE username=%s
      """, (form.address.data, form.name.data, form.ccnumber.data,hashedPassword, session['user']))

      cur.execute("select * from user where username=%s",[session['user']])
      results = cur.fetchall()
      emailAddress = results[0][3]
      mysql.connection.commit()
      cur.close()

      print(emailAddress)
      msg = Message('Profile Changed', sender="ugaonlinebookstore@gmail.com", recipients=[emailAddress])


      msg.body = 'Your profile has been updated.'

      mail.send(msg)

      return render_template('edit_profile.html', form=form, loggedIn=loggedIn, username=username, profileChanged=True)

   return render_template('edit_profile.html', form=form, loggedIn=loggedIn, username=username)

@app.route("/forgot_password", methods=['GET', 'POST']) #page with form that asks for user and email
def forgot_password():
   form = ForgotPass()
   if form.validate_on_submit():
      cur = mysql.connection.cursor()
      cur.execute("select * from user where username=%s", [form.username.data])
      results = cur.fetchall()
      cur.close()
      if form.email.data != results[0][3]:
         return render_template('forgot_password.html', form=form, incorrectInfo=True)#incorrect info
      else:
         token = s.dumps(form.email.data, salt='forgot-pass')
         print("TOKENTOKEN " + token)
         msg = Message('Change Password', sender="ugaonlinebookstore@gmail.com", recipients=[form.email.data])

         link = url_for('change_password_load', token=token, _external=True)

         msg.body = 'Change your password here {}'.format(link)
         
         mail.send(msg)

      return '<h1>check email to change password at ' + form.email.data + '</h1>'

   return render_template('forgot_password.html', form=form)

@app.route("/change_password", methods=['GET', 'POST']) #form that asks for what new password u want
def change_password():
   form = ChangePass()
   if form.validate_on_submit():
      cur = mysql.connection.cursor()
      print("HHHHHH")
      hashedPassword = generate_password_hash(form.newpassword.data, method='sha256')
      rowcount = cur.execute("select * from user where username like %s", [form.username.data])
      if rowcount > 0:
         cur.execute("""
         UPDATE user 
         SET password=%s 
         where username like %s""",(hashedPassword, form.username.data))
         mysql.connection.commit()
         cur.close()
         return redirect(url_for('login'))
      else:
         cur.close()
         return render_template('change_password.html', form=form, wrongUsername=True)
   return render_template('change_password.html', form=form)

@app.route("/change_password_load/<token>", methods=['GET', 'POST'])
def change_password_load(token):
   pass_ = s.loads(token, salt='forgot-pass', max_age=120)
   return redirect(url_for('change_password'))
# @app.route("/edit_profile_2", methods=['GET', 'POST'])
# def edit_profile_2():
#    form = EditForm()

#    return render_template('edit_profile_2.html', form=form)

@app.route("/return")
def returnBook():
   return render_template('return.html')

@app.route("/search")
def search():
   return render_template('search.html')

@app.route("/re_order")
def re_order():
   return render_template('re_order.html')

if __name__ == "__main__":
	app.run()