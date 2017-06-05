from flask import Flask
from flask import abort, redirect, url_for, render_template
from flask import request, session
import database
import json
app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = '|G\x8f\x7f\x02\xb87\x9cYai\xc4D\x11\xd4\xf4j>\x1a\x15\xdc\x95l\x1f'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uid = request.form['id']
        psw = request.form['psw']
        result = database.findUser("psw,name",uid)
        if len(result) > 0 and result[0][0]==psw :
            session['uid']= uid
            session['username']=result[0][1]
            return render_template("index.html", uname=session['username'])
        else:
            return render_template("hello.html", msg="User ID or Password wrong!")
    if 'uid' in session:
        return render_template("index.html", uname=session['username'])
    return render_template("hello.html")

@app.route("/signup",methods =['GET','POST'])
def signup():
    if request.method == 'POST':
        database.addUser(request.form['id'],request.form['psw'],request.form['name'],8)
        return render_template("hello.html", msg="Sign Up Succeed!")

@app.route('/logout')
def logout():
    session.pop('uid', None)
    session.pop('username', None)
    return redirect(url_for('index'))

#
@app.route("/searchpeople/",methods=['GET','POST'])
def searchpeople():
    if request.method == 'POST':
        searchText = request.data.split(';');
        print(searchText)
        uid=session['uid']
        frList=[]
        nofrList=[]
        noPerList=[]
        # for fid in searchText:
        #     t = database.findCon(uid,fid.strip())
        #     if len(t)>0:
        #         frList.append(t[0])
        #     else:
        #         t = database.findUser("id,name",fid)
        #         if len(t)>0:
        #             nofrList.append(t[0])
        #         else:
        #             noPerList.append(fid)
        result = {}
        result['friends']=frList
        result['strangers']=nofrList
        result['wrong']=noPerList
        return json.dumps(result)

@app.route("/addcon/")
def addcon():
    uid=session['uid']
    fid=request.args.get('id')
    fname=request.args.get('name')
    database.addCon(uid,fid,fname,"")
    return "success"

@app.route("/setnickname/")
def setnickname():
    uid=session['uid']
    fid=request.args.get('id')
    fname=request.args.get('name')
    fnickname = request.args.get('nickname')
    database.addCon(uid,fid,fname,fnickname)
    return "success"

@app.route("/getinv/",methods=['GET','POST'])
def getinv():
    if request.method == 'POST':
        return json.dumps(database.findInv("iid,ititle,istate,icount",session['uid']))

@app.route("/geteve/",methods=['GET','POST'])
def geteve():
    # to be modified
    if request.method == 'POST':
        return json.dumps(database.findInv("iid,ititle,istate,icount,icreator",session['uid']))

@app.route("/getcon/",methods=['GET','POST'])
def getcon():
    if request.method == 'POST':
        return json.dumps(database.findCon(session['uid']))

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
