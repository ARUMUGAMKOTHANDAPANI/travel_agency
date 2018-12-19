from flask import Flask , render_template , request,redirect,url_for
from flaskext.mysql import MySQL
app = Flask ( __name__ , static_url_path='/static' )

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'travel'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



db = mysql.connect ()
cursor = db.cursor ()
cursor.execute("SELECT * from user")
data = cursor.fetchone()
print(data)


def data_to_dict(cursor):
    columns = cursor.description
    result = [{columns[position][0]: column for position,column in enumerate(value)} for value in cursor.fetchall()]
    return result


@app.route ( '/' )
def index():
    return render_template ( 'index.html' )


@app.route ( '/booking' )
def booking():
    return render_template ( 'Booking.html' )


@app.route ( '/packages' )
def packages():
    return render_template ( 'Packages.html' )


@app.route ( '/contact', methods = ['GET','POST'] )
def contact():
    if request.method == 'GET':
        return render_template('Contact.html')
    if request.method == 'POST':
        name = request.form['name']
        email=request.form['email']
        message= request.form['message']
        add_contact = "INSERT INTO agency(name,email,message) VALUES (%s,%s,%s)"
        data_contact = (name,email,message)
        try:
            cursor.execute(add_contact,data_contact)
            db.commit()
        except Exception as ex:
            print(ex)
    return redirect ( url_for('contact') )


@app.route ( '/login' , methods=[ 'GET' , 'POST' ] )
def login():
    error =None
    if request.method =='POST':
        username_form = request.form['username']
        password_form = request.form['pass']
        cursor.execute("SELECT * FROM travel.user")
        data = cursor.fetchone()
        username = data[1]
        password = data[2]
        if username == username_form and password == password_form:
            return redirect(url_for('admin'))
        else:
            error = "INVALID CREDENTIALS"
    return render_template('login.html', error = error)


@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM agency")
    result= data_to_dict(cursor)
    print(result)
    return render_template('admin.html',result = result)


@app.route ('/delete/<id>')
def deleted(id):
       delete_query = "DELETE FROM agency WHERE `id`='%s';" % str(id)
       cursor.execute ( delete_query )
       db.commit ()
       return redirect ( url_for ( 'admin' ) )



if __name__ == '__main__':
    app.run ( debug=True )
