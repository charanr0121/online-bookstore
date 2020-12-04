from flask import Flask, render_template, jsonify, url_for, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateField
from wtforms.validators import InputRequired, Email, Length
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date
import yaml


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Secret!'
app.config.from_pyfile('config.cfg')

# loggedIn = False
username = None

db = yaml.load(open('db.yaml'), yaml.Loader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

bootstrap = Bootstrap(app)
mysql = MySQL(app)



class AddToCartForm(FlaskForm):
   isbn=StringField()

class AddPromotion(FlaskForm):
   value = StringField('value', validators=[InputRequired(), Length(min=1)])
   restrictions = StringField('restrictions', validators=[InputRequired(), Length(min=1)])
   end_date = DateField("End date", validators=[DataRequired(message="You must enter an end date.")], format='%Y-%m-%d')

class SearchForm(FlaskForm):
   query = StringField('Search by title, ISBN, author, etc.', validators=[InputRequired(), Length(min=1)])

class RemoveBookForm(FlaskForm):
   isbn = StringField('ISBN', validators=[InputRequired(), Length(min=10, max=15)])

class RemovePromotion(FlaskForm):
   id = StringField('Promotion id', validators=[InputRequired(), Length(min=1)])

class SubForm(FlaskForm):
   username = StringField('Username', validators=[Length(min=0, max=100)])

class AddBookForm(FlaskForm):
   isbn = StringField('ISBN', validators=[InputRequired(), Length(min=10, max=15)])
   title = StringField('Title', validators=[InputRequired(), Length(min=1, max=45)])
   sell_price = IntegerField('Sell Price', validators=[InputRequired()])
   min_threshold = IntegerField('Quantity', validators=[InputRequired()])
   category = StringField('Category', validators=[InputRequired(), Length(min=0, max=45)])
   author = StringField('Author', validators=[InputRequired(), Length(min=0, max=45)])

class LoginForm(FlaskForm):
   username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
   password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
   remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
   email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
   name = StringField('full name', validators=[InputRequired(), Length(min=1, max=100)])
   username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
   phone = StringField('phone number', validators=[InputRequired(), Length(min=7, max=15)])
   password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
   ccnumber = StringField('credit card number', validators=[])
   address = StringField('address', validators=[])

class NameForm(FlaskForm):
      name = StringField('full name', validators=[InputRequired(), Length(min=1, max=100)])

class AddressForm(FlaskForm):
      address = StringField('address', validators=[InputRequired(), Length(min=2, max=80)])

class CCNumberForm(FlaskForm):
      ccnumber = StringField('credit card number', validators=[InputRequired(), Length(min=14, max=18)])

class PassForm(FlaskForm):
   currpassword = PasswordField('current password', validators=[InputRequired(), Length(min=8, max=80)])
   newpassword = PasswordField('new password', validators=[InputRequired(), Length(min=8, max=80)])

class AddPromoForm(FlaskForm):
   code = StringField('Promo Code', validators=[Length(min=5, max=80)])
   value = IntegerField('Percent Off', validators=[InputRequired()])
   expiry_date = DateField('Expiry Date')



class ForgotPass(FlaskForm):
   username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
   email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

class SuspendUserForm(FlaskForm):
   username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])

class UnsuspendUserForm(FlaskForm):
   username = StringField('Usssername', validators=[InputRequired(), Length(min=4, max=15)])

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
      print(results[0][8]) #PHONE
      

      # This is where we would get the remaining feilds from the database
      # And set the corresponding values so that we can acsess them from the html file

      
      
      


@app.route("/")
@app.route("/home")
def home():
   
   searchform = SearchForm()

   cur = mysql.connection.cursor()
   rowcount = cur.execute("select * from book")
   results = cur.fetchall()
   cur.close()
   return render_template('index.html', books=results, searchform=searchform)

@app.route('/removeFromCart', methods=['GET','POST'])
def removeFromCart():
   session['cartQty'] -= 1
   cur = mysql.connection.cursor()
   cur.execute("select * from book where isbn=%s", [request.form['isbn']])
   res = cur.fetchall()
   print("DD")
   print(request.form['isbn'])
   print(res)
   bookPrice = res[0][3]

   cur.execute("select * from pendingOrder where (user=%s and isbn=%s)", [session['user'], request.form['isbn']])
   book = cur.fetchall()
   if book[0][2] == 1: #if qty is 1
      cur.execute("DELETE FROM pendingOrder WHERE (user=%s and isbn=%s);",[session['user'], request.form['isbn']])
   else:
      cur.execute("update pendingOrder set qty=%s where (user=%s and isbn=%s)", [ book[0][2]-1, session['user'], request.form['isbn']])
      cur.execute("update pendingOrder set total=%s where (user=%s and isbn=%s)", [ book[0][3] - bookPrice, session['user'], request.form['isbn']])
   mysql.connection.commit()
   cur.close()
   return redirect(url_for("view_cart"))




@app.route('/addToCart', methods=['GET', 'POST'])
def addToCart():
   session['cartQty'] += 1
   print(request.form['isbn'])
   cur = mysql.connection.cursor()
   cur.execute("select * from book where isbn=%s", [request.form['isbn']])
   res = cur.fetchall()
   price = res[0][3]
   print(res)
   if res[0][10] <= 0:
      return redirect(request.referrer)
   rowcount = cur.execute("select * from pendingOrder where (user=%s and isbn=%s)", [session['user'], request.form['isbn']])
   if rowcount == 0: #generate new orderID
   #    session['orderID'] = 
      cur.execute("insert into pendingOrder(user, isbn, qty, total) values(%s,%s,%s,%s)", [session['user'], request.form['isbn'], 1, price])
   else:
      cur.execute("select * from pendingOrder where (user=%s and isbn=%s)", [session['user'], request.form['isbn']])
      book = cur.fetchall()

      cur.execute("update pendingOrder set qty=%s where (user=%s and isbn=%s)", [ book[0][2]+1, session['user'], request.form['isbn']])
      cur.execute("update pendingOrder set total=%s where (user=%s and isbn=%s)", [ price + book[0][3], session['user'], request.form['isbn']])

   mysql.connection.commit()
   cur.close()

   return redirect(request.referrer)

@app.route("/logout")
def logout():
   session['user'] = None
   session['loggedIn'] = False
   session['isAdmin'] = False
   session['cartQty'] = 0

   return redirect(url_for('home'))

@app.route("/login", methods=['GET', 'POST'])
def login():
   session['cartQty'] = 0
   if 'loggedIn' in session and session['loggedIn']:
      return redirect(url_for('home'))
   form = LoginForm()

   if form.validate_on_submit():
      cur = mysql.connection.cursor()
      rowcount = cur.execute("select * from user where username=%s",[form.username.data])
      results = cur.fetchall()
      cur.close()
      print("RESULTS")
      if rowcount > 0:
         print(results[0][2])
         if (results[0][10]==1):
            return '<h1>this account has been suspended.<h1>'
         if(results[0][4]==1):
            if check_password_hash(results[0][2], form.password.data):
               user = User(form.username.data)
               session['user'] = form.username.data
               session['loggedIn'] = True
               session['email'] = results[0][3]
               session['cc'] = results[0][5]
               session['add'] = results[0][6]
               session['name'] = results[0][7]
               session['phone'] = results[0][8]
               
               if results[0][9]==1:
                  session['isAdmin'] = True
                  return redirect(url_for('admin_page'))
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
      try:
         cur = mysql.connection.cursor()
         hashedPassword = generate_password_hash(form.password.data, method='sha256')
         cur.execute("INSERT INTO user(username, email, password, phone, address, name) VALUES(%s, %s, %s, %s, %s, %s)",(form.username.data, form.email.data, hashedPassword, form.phone.data, form.address.data, form.name.data))
         mysql.connection.commit()
         token = s.dumps(form.email.data, salt='email-confirm')

         print("TOKENTOKEN " + token)
         msg = Message('Confirm Email', sender="ugaonlinebookstore@gmail.com", recipients=[form.email.data])

         link = url_for('confirm_email', token=token, _external=True)

         msg.body = 'Your confirmation link is {}'.format(link)

         mail.send(msg)

         return '<h1>check for confirmation email at ' + form.email.data + '</h1>'

      except:
         print("DUPLICATE ENTRY")
         return render_template('signup.html', form=form, duplicateEntry=True)

      cur.close()
   
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

@app.route("/about")
def about():
   return render_template('about.html')


@app.route("/checkout")
def checkout():
   return render_template('checkout.html')



@app.route("/shop", methods=['GET', 'POST'])
def shop():
   cur = mysql.connection.cursor()
   cur.execute("select * from book")
   books = cur.fetchall()
   cur.close()
   return render_template('shop.html', books= books)


@app.route("/construction")
def construction():
   return render_template('construction.html')

@app.route("/view_cart")
def view_cart():

   cur = mysql.connection.cursor()
   cur.execute("select * from pendingOrder where user=%s", [session['user']])
   cart = cur.fetchall()
   totalPrice = 0
   for book in cart:
      totalPrice += book[3]
   return render_template("view_cart.html", cart=cart, totalPrice=totalPrice)
   

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
   if 'loggedIn' not in session or session['loggedIn'] == False:
      return redirect(url_for('login'))
   nameform = NameForm()
   addressform = AddressForm()
   passform = PassForm()
   subform = SubForm()
   ccnumberform = CCNumberForm()

   if nameform.validate_on_submit():
      cur = mysql.connection.cursor()
      cur.execute("update user set name=%s where username=%s", (nameform.name.data, session['user']))
      mysql.connection.commit()
      cur.close()
      return redirect(url_for("edit_profile"))

   if addressform.validate_on_submit():
      cur = mysql.connection.cursor()
      cur.execute("update user set address=%s where username=%s", (addressform.address.data, session['user']))
      mysql.connection.commit()
      cur.close()
      return redirect(url_for("edit_profile"))

   if subform.validate_on_submit():
      cur = mysql.connection.cursor()

      if request.form['submit_button'] == 'subscribe':
         cur.execute("update user set subscribed=1 where username=%s",[session['user']])
         mysql.connection.commit()
         cur.close()
         return redirect(url_for("edit_profile"))
      elif request.form['submit_button'] == 'unsubscribe':
         cur.execute("update user set subscribed=0 where username=%s",[session['user']])
         mysql.connection.commit()
         cur.close()
         return redirect(url_for("edit_profile"))

   if passform.validate_on_submit():
      cur = mysql.connection.cursor()

      cur.execute("select * from user where username=%s",[session['user']])
      results = cur.fetchall()
      if check_password_hash(results[0][2], passform.currpassword.data):
         hashedPassword = generate_password_hash(passform.newpassword.data, method='sha256')

         cur.execute("update user set password=%s where username=%s", (hashedPassword, session['user']))
      mysql.connection.commit()
      cur.close()
      return redirect(url_for("edit_profile"))

   if ccnumberform.validate_on_submit():
      cur = mysql.connection.cursor()
      cur.execute("update user set ccnumber=%s where username=%s", (ccnumberform.ccnumber.data, session['user']))
      mysql.connection.commit()
      cur.close()
      return redirect(url_for("edit_profile"))
      # elif request.form['submit-button'] == 'change-pass':

      # elif request.form['submit-button'] == 'change-address':

      # elif request.form['submit-button'] == 'change-ccnumber':


   cur = mysql.connection.cursor()
   cur.execute("select * from user where username=%s", [session['user']])
   info = cur.fetchall()
   cur.close()

   return render_template('edit_profile.html', nameform=nameform, subform=subform, ccnumberform=ccnumberform, addressform=addressform, passform=passform, info=info)

# def edit_profile():
#    form = EditForm()

#    if form.validate_on_submit():
#       cur = mysql.connection.cursor()
#       hashedPassword = generate_password_hash(form.newpassword.data, method='sha256')
#       cur.execute("""
#          UPDATE user
#          SET address=%s, name=%s, ccnumber=%s, password=%s
#          WHERE username=%s
#       """, (form.address.data, form.name.data, form.ccnumber.data,hashedPassword, session['user']))

#       cur.execute("select * from user where username=%s",[session['user']])
#       results = cur.fetchall()
#       emailAddress = results[0][3]
#       mysql.connection.commit()
#       cur.close()

#       print(emailAddress)
#       msg = Message('Profile Changed', sender="ugaonlinebookstore@gmail.com", recipients=[emailAddress])


#       msg.body = 'Your profile has been updated.'

#       mail.send(msg)

#       return render_template('edit_profile.html', form=form, loggedIn=loggedIn, username=username, profileChanged=True)

#    return render_template('edit_profile.html', form=form, loggedIn=loggedIn, username=username)

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

@app.route("/manage_books", methods=['GET','POST'])
def manage_books():

   if 'isAdmin' not in session or session['isAdmin'] == False:
      return redirect(url_for('home'))

   form = RemoveBookForm()
   form2 = AddBookForm()

   cur = mysql.connection.cursor()
   cur.execute("select * from book")
   books = cur.fetchall()
   cur.close()
   if form2.validate_on_submit() and form.validate_on_submit():
      print("madddd")

   if form2.validate_on_submit():
      print("add book")
      cur = mysql.connection.cursor()
      try:
         print("insert into book (isbn,author,category,title,sell_price,min_threshold) values(%s, %s, %s, %s, %s, %s)", (form2.isbn.data, form2.author.data, form2.category.data, form2.title.data, form2.sell_price.data, form2.min_threshold.data))
         cur.execute("insert into book (isbn,author,category,title,sell_price,min_threshold) values(%s, %s, %s, %s, %s, %s)", (form2.isbn.data, form2.author.data, form2.category.data, form2.title.data, form2.sell_price.data, form2.min_threshold.data))
         mysql.connection.commit()
         cur.close()
         return redirect(url_for('manage_books'))
      except:
         cur.close()
         return render_template('manage_books.html', books=books, form=form, form2=form2, duplicateEntry=True)

   if form.validate_on_submit():
      print("remove book")
      cur = mysql.connection.cursor()

      rowcount = cur.execute("select * from book where isbn=%s", [form.isbn.data])
      book = cur.fetchall()
      if rowcount > 0:
         cur.execute("insert into archivedbook (isbn,author,category,title,sell_price,min_threshold) values(%s, %s, %s, %s, %s, %s)", (book[0][0],book[0][5],book[0][0],book[0][1],book[0][3],book[0][10]))
         cur.execute("DELETE FROM book WHERE isbn=%s;",[form.isbn.data])
         mysql.connection.commit()
         cur.close()
         return redirect(url_for('manage_books'))
      else:
         cur.close()
         return render_template("manage_books.html", books=books, form=form, form2=form2, invalidISBN=True)
      
   return render_template('manage_books.html', books=books, form=form, form2=form2)

@app.route("/return")
def returnBook():
   return render_template('return.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
   # searchform = SearchForm()
   # print("JERE")
   if request.method == "GET":
      # print(request.args)
      # print(request.args['search-query'])
      # print("JERE2")
      cur = mysql.connection.cursor()
      queryString = '%' + request.args['search-query'] + '%'
      # print(queryString)
      cur.execute("select * from book where (isbn like %s or title like %s or category like %s or author like %s)", [queryString,queryString,queryString,queryString])
      searchResults = cur.fetchall()
      # print(searchResults)

   return render_template('search.html', searchResults=searchResults)

@app.route("/re_order")
def re_order():
   return render_template('re_order.html')

@app.route("/admin_page")
def admin_page():
   if 'isAdmin' not in session or session['isAdmin'] == False:
      return redirect(url_for('home'))
   return render_template('admin_page.html')

@app.route("/manage_users", methods=['GET','POST'])
def manage_users():

   if 'isAdmin' not in session or session['isAdmin'] == False:
      return redirect(url_for('home'))

   form = SuspendUserForm()

   cur = mysql.connection.cursor()
   cur.execute("select * from user")
   users = cur.fetchall()


   cur.close()

   if form.validate_on_submit():
      
      cur = mysql.connection.cursor()

      if request.form['submit_button'] == 'suspend': 
         print("suspend")
         cur.execute("UPDATE user SET suspended=1 where username like %s",[form.username.data])
         mysql.connection.commit()
         cur.close()
      elif request.form['submit_button'] == 'unsuspend': 
         print("unsuspend")
         cur.execute("UPDATE user SET suspended=0 where username like %s",[form.username.data])
         mysql.connection.commit()
         cur.close()
      elif request.form['submit_button'] == 'promote': 
         print("promote")
         cur.execute("select admin from user where username like %s",[form.username.data])
         level = cur.fetchall()[0][0]

         if level == 1:
            level = level
         elif level == 2:
            level = 1
         else:
            level = 2
         cur.execute("UPDATE user SET admin=" + str(level) + " where username like %s",[form.username.data])
         mysql.connection.commit()
         cur.close()
      elif request.form['submit_button'] == 'demote':
         print('demote')
         cur.execute("select admin from user where username like %s",[form.username.data])
         level = cur.fetchall()[0][0]

         if level == 1:
            level = 2
         elif level == 2:
            level = 0
            
         cur.execute("UPDATE user SET admin=" + str(level) + " where username like %s",[form.username.data])
         mysql.connection.commit()
         cur.close()
         
      return redirect(url_for('manage_users'))



   return render_template('manage_users.html', users=users, form=form)

@app.route('/books')
def books():
   cur = mysql.connection.cursor()
   cur.execute("select * from book")
   books = cur.fetchall()
   cur.close()
   return render_template('books.html', books=books)

@app.route('/books/<isbn>')
def book_landing_page(isbn):
   cur = mysql.connection.cursor()
   cur.execute("select * from book where isbn=%s", [isbn])
   bookInfo = cur.fetchall()
   print(bookInfo)
   cur.close()
   return render_template('book_landing_page.html', bookInfo=bookInfo)

@app.route('/manage_promos', methods=['GET','POST'])
def manage_promos():

   if 'isAdmin' not in session or session['isAdmin'] == False:
      return redirect(url_for('home'))


   form = AddPromoForm()

   cur = mysql.connection.cursor()
   cur.execute("select * from promotion")
   promotions = cur.fetchall()
   cur.close()

   if form.validate_on_submit():
      print(form.expiry_date.data)
      cur = mysql.connection.cursor()
      cur.execute("insert into promotion (promocode,val,expiry_date) values(%s,%s,%s)", [form.code.data, form.value.data, form.expiry_date.data])
      mysql.connection.commit()
      cur.execute("select email from user where subscribed=1")
      results = cur.fetchall()
      # print(mailingList)
      mailingList = []
      for mail1 in results:
         for mail2 in mail1:
            mailingList.append(mail2)

      print(mailingList)
      cur.close()

      msg = Message('New Promotion!', sender="ugaonlinebookstore@gmail.com", recipients=mailingList)


      msg.body = 'A new promotion has been added! Use promo code ' + form.code.data + ' for ' + str(form.value.data) + '% off your next purchase! Make sure you use it by ' + str(form.expiry_date.data) + '!'

      mail.send(msg)

      return redirect(url_for('manage_promos'))

   return render_template('manage_promos.html', form=form, promotions=promotions)

if __name__ == "__main__":
	app.run()