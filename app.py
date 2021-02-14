#app.py
from flask import Flask, request, session, redirect, url_for, render_template

from flaskext.mysql import MySQL

import pymysql 
from datetime import date

import re 
import bcrypt
 
app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'cairocoders-ednalan'
 
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'blogs'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



# @app.route('/')
# def home():
    
#     return render_template('home.html')


@app.route('/register',methods=['GET', 'POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        signup=request.form
        full_name=signup['fullname']
        user_name=signup['username']
        e_mail=signup['email']
        p_hone=signup['phone']
        pass_word=signup['password']
        # hash_password = bcrypt.hashpw(pass_word, bcrypt.gensalt())

        # cursor.execute("insert into register(fullname,username,email,phone,password)"values(%s,%s,%s,%d,%s))
        cursor.execute('INSERT INTO register VALUES ( %s,%s, %s, %s,%s,%s)', ('',full_name,user_name,e_mail,p_hone,pass_word )) 
        conn.commit()
        cursor.close()

        return render_template('login.html')
    else:
        return  render_template('register.html')      

       
    # return render_template('register.html')    


  

    


@app.route('/login',methods=["GET","POST"])
def login():
    
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM register WHERE username=%s",(username))
        user = cursor.fetchone()
        print(user)
        print('helllo')
   
        # cursor.close()

        if user:
            if  password == user['password']:
                session['name'] = user['username']
                session['email'] = user['email']
                return redirect("/dashboard")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")

@app.route('/dashboard')
def dash():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM posts")
    account = cursor.fetchall()


    
    
    return render_template("dash.html",account=account)




@app.route('/',methods=["GET","POST"])
def posts():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # if request.method == 'POST':
        # post_title = request.form['title']
        # post_author = request.form['author']
        # post_content =request.form['content']
    cursor.execute("SELECT * FROM posts")
    account = cursor.fetchall()

    return render_template('home.html',account=account)
    # else:
    #     return redirect('/newpost')    


        
    #     new_post = BlogPost(title = post_title,content = post_content,author = post_author)
    #     db.session.add(new_post)
    #     db.session.commit()
    #     return redirect('/posts')
    # else:
    #     all_posts=BlogPost.query.order_by(BlogPost.date_posted).all()    
      


@app.route('/newpost',methods=["GET","POST"])
def newpost():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        signup=request.form
        title=signup['title']
        author=signup['author']
        content=signup['content']
        today = date.today()
      


        # p_hone=signup['phone']
        # pass_word=signup['password']
        # hash_password = bcrypt.hashpw(pass_word, bcrypt.gensalt())

        # cursor.execute("insert into register(fullname,username,email,phone,password)"values(%s,%s,%s,%d,%s))
        #asks
        cursor.execute('INSERT INTO posts VALUES ( %s,%s, %s,%s,%s)', ('',title,author,content,today )) 
        conn.commit()
        # cursor.execute("SELECT * FROM posts ")
        # user = cursor.fetchall()
        cursor.close()
        return redirect('/dashboard')
    # else:

    return render_template('new_post.html')  



@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print("dfdpy")
    print(id)

    
    sql = "DELETE FROM posts WHERE id = '%s'"
    adr = (id, )
    cursor.execute(sql, adr)

    # sql = "DELETE FROM posts WHERE id = id"
    

    # cursor.execute(sql)
    print(cursor._last_executed)
    conn.commit()
    cursor.close()


    return redirect('/dashboard')             

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # cursor.execute("SELECT * FROM posts")
    
    sql = "SELECT * FROM posts WHERE id = '%s'"
    adr = (id, )
    cursor.execute(sql, adr)
    post = cursor.fetchone()

    print(post)

   
    if request.method == 'POST':
        
        title =request.form['title']
        author =request.form['author']
        content =request.form['content']
    

        conn.commit()
        cursor.close()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute ("UPDATE posts SET title='%s', author='%s', content='%s' WHERE id='%s' " % (title, author, content, id))
        conn.commit()
        conn.close()
        print("updated successfully")
        print(cursor._last_executed)



        
       
        return redirect('/dashboard')
    else:
        return render_template('edit.html',post=post)  

if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)






