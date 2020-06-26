from flask import Flask,redirect,render_template,url_for,session,request
import sqlite3
import string
import random


app=Flask(__name__)

def randomno():
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(6)))


@app.route('/', methods=['GET', 'POST'])
def index():
    session['uid']="ashish"
    if "uid" in session:
        return redirect(url_for('user'))
    else:
        return render_template("index.html")

@app.route('/user', methods=['GET', 'POST'])
def user():
    if "uid" in session:
        userkey=session['uid']
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
        return render_template("index.html")



@app.route('/user/<u>', methods=['GET', 'POST'])
def send(u):
    if request.method=="GET":
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        s='SELECT * from users WHERE uniquelink="'+str(u)+'"'
        c.execute(s)
        all=c.fetchone()
        print(all)
        if all==None:
            return render_template("index.html")
        else:
            name=all[1]
            return render_template("send_message.html",name=name)





if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True,port=80)
