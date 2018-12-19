from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/booking')
def booking():
   return render_template('Booking.html')


@app.route('/packages')
def packages():
   return render_template('Packages.html')


@app.route('/contact')
def contact():
   return render_template('Contact.html')

@app.route('/login')
def login():
   return render_template('login.html')

if __name__ == '__main__':
   app.run(debug = True)
