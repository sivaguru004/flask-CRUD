from flask import Flask,render_template, url_for, redirect,request,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#mysql connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='************'
app.config['MYSQL_DB']='crud'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql = MySQL(app)

#loading Home Page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = 'select * from users'
    con.execute(sql)
    res = con.fetchall()
    return render_template('home.html', data = res)

#Add User
@app.route("/AddUser", methods=['GET','POST'])
def adduser():
    if request.method=='POST':
        name =  request.form['name']
        age =  request.form['age']
        city =  request.form['city']
        con = mysql.connection.cursor()
        sql = 'insert into users (name,age,city) values (%s,%s,%s)'
        con.execute(sql, [name,age,city])
        mysql.connection.commit()
        con.close()
        flash('User Detail Added Successfully')
        return redirect(url_for('home'))
    return render_template('user.html')

#Edit User
@app.route('/editUser/<int:id>', methods=['GET', 'POST'])
def editUser(id):
    con = mysql.connection.cursor()
    if request.method=='POST':
        name =  request.form['name']
        age =  request.form['age']
        city =  request.form['city']
        sql = 'update users set name=%s, age=%s, city=%s where ID=%s'
        con.execute(sql, [name,age,city,id])
        mysql.connection.commit()
        con.close()
        flash('User Detail Updated Successfully')
        return redirect(url_for('home'))
    
    sql = 'select * from users where ID=%s'
    con.execute(sql, [id])
    res = con.fetchone()
    return render_template('editUser.html', data=res)

#delete user
@app.route('/delete/<int:id>', methods=['GET','POST'])
def deleteuser(id):
    con = mysql.connection.cursor()
    sql = 'delete from users where ID=%s'
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    flash('User Detail Deleted Successfully')
    return redirect(url_for('home'))

if (__name__=='__main__'):
    app.secret_key='user123'
    app.run(debug=True)