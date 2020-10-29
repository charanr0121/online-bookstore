from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
	return render_template('index.html')

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/books")
def books():
	return render_template('books.html')

@app.route("/construction")
def construction():
   return render_template('construction.html')

@app.route("/edit_profile")
def edit_profile():
   return render_template('edit_profile.html')

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