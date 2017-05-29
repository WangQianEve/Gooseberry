from flask import Flask
from flask import abort, redirect, url_for, render_template
from flask import request, session
import database
app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = '|G\x8f\x7f\x02\xb87\x9cYai\xc4D\x11\xd4\xf4j>\x1a\x15\xdc\x95l\x1f'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uid = request.form['uid']
        udata = database.findUser("uid,uname",uid)
        if(len(udata)!=0):
            session['uid'] = udata[0][0]
            session['username'] = udata[0][1]
            render_template("index.html", uname=session['username'])
        else:
            render_template("hello.html", msg="No Such User")
    if 'uid' in session:
        return render_template("index.html", uname=session['username'])
    return render_template("hello.html")

@app.route("/getinv/",methods=['GET','POST'])
def getinv():
    if request.method == 'POST':
        return database.findInv("iid,ititle,istate,icount",session['uid'])
        
@app.route('/logout')
def logout():
    session.pop('uid', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# evoked by user.html
@app.route("/createInvitation/")
def createInvitation():
    id=002
    # temp
    return redirect(url_for('invitation', inv_id=id, on_create=True ))
    # if success:
    #     return redirect(url_for('invitation', inv_id=id, on_create=True ))
    # else:
    #     return 0

@app.route("/user/", methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        # add into database
        print(request.form['title'])
        return "001"
    else:
    # if not signed-in:
    #     return redirect(url_for('hello'))
    # else:
        return render_template("user.html")

@app.route("/invitation/<inv_id>")
def invitation(inv_id):
    invitation = 'inv'
    return render_template("invitation.html", data=invitation, on_create = True)
    # if not signed-in:
    #     return redirect(url_for('hello'))
    # else:
    #     if id valid:
    #         get invitation
    #         return render_template("invitation.html", data=invitation, on_create = on_create)
    #     else:
    #         return "Invitation does not exist!"

@app.route("/about/")
def about():
    return "Under construction"

@app.route("/tutorial/")
def tutorial():
    return "Under construction"

@app.route("/timetable/")
def timetable():
    return render_template("timetable_test.html")

@app.route("/tablesuperimposition/")
def tablesuperimposition():
    return render_template("table_superimposition.html")

if __name__ == "__main__":
    app.run()
