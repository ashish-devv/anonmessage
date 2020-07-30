from flask import Flask,redirect,render_template,url_for,request,make_response
import sqlite3
import string
import random
import time


app=Flask(__name__)

def randomno():
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(6)))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=="GET":
        if "uid" in request.cookies:
            return redirect(url_for('user'))
        else:
            return render_template("index.html")
    if request.method=="POST":
        name=request.form['nm']
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        unique=randomno()
        s='INSERT INTO users (name,uniquelink)VALUES("'+str(name)+'","'+str(unique)+'")'
        c.execute(s)
        all=c.fetchone()
        conn.commit()
        c.close()
        resp = make_response(redirect(url_for("index"))) 
        resp.set_cookie("uid",unique)
        return resp

@app.route('/user', methods=['GET', 'POST'])
def user():
    if "uid" in request.cookies:
        userkey=request.cookies.get("uid")  
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        s='SELECT * from users WHERE uniquelink="'+str(userkey)+'"'
        c.execute(s)
        all=c.fetchone()
        link=request.base_url+"/"+str(all[2])
        username=str(all[1])
        s='SELECT msg FROM messages WHERE uniqueusers="'+str(userkey)+'"'
        c.execute(s)
        ms=c.fetchall()
        c.close()
        print(ms)
        return render_template("user.html",link=link,username=username,ms=ms)
    else:
        return redirect(url_for("index"))



@app.route('/user/<u>', methods=['GET', 'POST'])
def send(u):
    if request.method=="GET":
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        s='SELECT * from users WHERE uniquelink="'+str(u)+'"'
        c.execute(s)
        all=c.fetchone()
        c.close()
        print(all)
        if all==None:
            return redirect(url_for("index"))
        else:
            name=all[1]
            uniq=all[2]
            return render_template("send_message.html",name=name,uniq=uniq)
    if request.method=="POST":
        mssg=request.form['m']
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        timeofmessage=time.ctime()
        s='INSERT INTO messages (uniqueusers,msg,datetime)VALUES("'+str(u)+'","'+str(mssg)+'","'+timeofmessage+'")'
        print(s)
        c.execute(s)
        all=c.fetchone()
        conn.commit()
        c.close()
        return redirect(url_for("index"))




if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=False)
