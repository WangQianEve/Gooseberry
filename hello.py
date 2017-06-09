from flask import Flask
from flask import abort, redirect, url_for, render_template, jsonify, request, session
import json, time,datetime
# my module
import database

app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = '|G\x8f\x7f\x02\xb87\x9cYai\xc4D\x11\xd4\xf4j>\x1a\x15\xdc\x95l\x1f'

#Make some data to use
lineNum = 24
time_amount = 7*lineNum
cur_date = time.strftime('%y%m%d0000',time.localtime(time.time()))

### inner functions
def count_time_unit(t):
    time_num = 0
    d1 = datetime.datetime(int('20'+t[0:2]), int(t[2:4]), int(t[4:6]))
    d2 = datetime.datetime(int('20'+cur_date[0:2]), int(cur_date[2:4]), int(cur_date[4:6]))
    time_num = (d1-d2).days * lineNum + int(t[6:8])*lineNum/24
    return time_num

def calc_time(time_num):
    t = 0
    d1 = datetime.datetime(int('20'+cur_date[0:2]), int(cur_date[2:4]), int(cur_date[4:6]))
    d2 = (d1 + datetime.timedelta(days=time_num/lineNum)).strftime('%y%m%d')
    t = d2 + '%02d' %(time_num % lineNum) + '00'
    return t

def get_table_info_by_usr(usr):
    table_data = {"time" : []}
    if 'uid' in session:
        user_data = database.findTime(usr,cur_date)
        for i in user_data:
            start_time = i[1].strftime('%y%m%d%H00')
            start_num = count_time_unit(start_time)
            end_time = i[2].strftime('%y%m%d%H00')
            end_num = count_time_unit(end_time)
            act = {"title":i[0],"start":start_num,"end":end_num}
            table_data["time"].append(act)
    return table_data

def cal_color(usrlist):
    tmpdict={}
    for u in usrlist:
        user_data = database.findTime(u,cur_date)
        for i in user_data:
            start_time = i[1].strftime('%y%m%d%H00')
            start_num = count_time_unit(start_time)
            end_time = i[2].strftime('%y%m%d%H00')
            end_num = count_time_unit(end_time)
            for k in range(start_num, end_num + 1):
                if k < 0:
                    continue;
                if not str(k) in tmpdict:
                    tmpdict[str(k)] = 1
                else:
                    tmpdict[str(k)] += 1
    return tmpdict

# [page] hello.html or index.html
@app.route("/", methods=['GET', 'POST'])
def index():
    #Update the date
    cur_date=time.strftime('%y%m%d0000',time.localtime(time.time()))
    friendlist = []
    if request.method == 'POST':
        uid = request.form['id']
        psw = request.form['psw']
        result = database.findUser("psw,name",uid)
        if len(result) > 0 and result[0][0]==psw :
            session['uid']= uid
            session['username']=result[0][1]
            table_data = json.dumps(get_table_info_by_usr(session['uid']))
            friendlist = database.findCon(session['uid'])
            usrlist = []
            bkdata= json.dumps(cal_color(usrlist))
            return render_template("index.html", uid=session['uid'], uname=session['username'],bgcolor = bkdata,table_data=table_data,friendlist = friendlist,lineNum = lineNum)
        else:
            return render_template("hello.html", msg="User ID or Password wrong!")
    if 'uid' in session:
        table_data = json.dumps(get_table_info_by_usr(session['uid']))
        friendlist = database.findCon(session['uid'])
        usrlist = []
        bkdata= json.dumps(cal_color(usrlist));
        return render_template("index.html", uid=session['uid'], uname=session['username'],bgcolor = bkdata,table_data=table_data,friendlist = friendlist, lineNum = lineNum)
    return render_template("hello.html")

@app.route("/signup",methods =['GET','POST']) # to index
def signup():
    if request.method == 'POST':
        if(len(database.findUser('id',request.form['id']))>0):
            return render_template("hello.html", msg="User Exists! Please Log in~")
        if(isinstance(database.addUser(request.form['id'],request.form['psw'],request.form['name'],8),tuple)):
            return render_template("hello.html", msg="Sign Up Succeed!")
        else:
            return render_template("hello.html", msg="Something Wrong!")

@app.route('/logout') # to index
def logout():
    session.pop('uid', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# [page] invitation.html
@app.route("/invitation/<inv_id>")
def invitation(inv_id):
    if 'uid' not in session:
        return redirect(url_for('index'))
    invdata = database.findInvById("title,status,creator,description,options,members,startdate,final",inv_id)
    if(len(invdata))==0:
        return "Invitation does not exist!"
    mopt = database.findOpp(inv_id,session['uid'])
    return render_template("invitation.html", moptions=json.dumps(mopt), inv=inv_id, uid=session['uid'], uname=session['username'], data=json.dumps(invdata), on_create = True)

# update one's choice about an invitation
@app.route("/modiInv/") # to invitation
def modiInv():
    invId = request.args.get('invid')
    options = json.loads(request.args.get('opt'))
    uid = session['uid']
    database.delOpp(invId,uid)
    for op in options:
        database.addOpp(invId,uid,op)
    return redirect(url_for('invitation',inv_id=invId))

# join invitation
@app.route("/joinInv/") # to invitation
def joinInv():
    invId = request.args.get('invid')
    options = json.loads(request.args.get('opt'))
    uid = session['uid']
    database.invAddMember(invId,uid)
    database.userAddInv(invId,uid)
    for op in options:
        database.addOpp(invId,uid,op)
    return redirect(url_for('invitation',inv_id=invId))

# settle invitation
@app.route("/setInv/") # to invitation
def setInv():
    invId = request.args.get('invid')
    options = json.loads(request.args.get('opt'))
    uid = session['uid']
    database.invSettle(invId,options)
    return redirect(url_for('invitation',inv_id=invId))

# exit an invitation
@app.route("/exitInv/",methods=['GET','POST']) # to invitation
def exitInv():
    invId = request.args.get('invid')
    uid = session['uid']
    database.invDelMember(invId,uid)
    database.userDelInv(invId,uid)
    database.delOpp(invId,uid)
    return redirect(url_for('invitation',inv_id=invId))

# delete an invitation
@app.route("/delInv/<inv_id>") # to invitation
def delInv(inv_id):
    database.delInv(inv_id)
    database.delOpp(inv_id)
    return redirect(url_for('index'))

# [page] under construction
@app.route("/about/")
def about():
    return "Under construction"

# [page] tutorial.html
@app.route("/tutorial/")
def tutorial():
    return render_template("tutorial.html")

# reply search result
@app.route("/searchpeople/",methods=['GET','POST'])
def searchpeople():
    if request.method == 'POST':
        searchText = request.values.get('ids').split(';');
        uid=session['uid']
        frList=[]
        nofrList=[]
        noPerList=[]
        for fid in searchText:
            t = database.relation(uid,fid.strip())
            if len(t)>0:
                frList.append(t[0])
            else:
                t = database.findUser("id,name",fid)
                if len(t)>0:
                    nofrList.append(t[0])
                else:
                    noPerList.append(fid)
        result = {}
        result['friends']=frList
        result['strangers']=nofrList
        result['wrong']=noPerList
        print "-----resulf of searchpeople()-----"
        print result
        return json.dumps(result)

# add friend and return contact list
@app.route("/addcon/",methods=['GET','POST'])
def addcon():
    if request.method == 'POST':
        uid=session['uid']
        fid=request.form['id']
        fname=request.form['name']
        database.addCon(uid,fid,fname,"")
        return json.dumps(database.findCon(uid))

# delete friend and return contact list
@app.route("/delcon/",methods=['GET','POST'])
def delcon():
    if request.method == 'POST':
        uid=session['uid']
        fid=request.form['id']
        database.delCon(uid,fid)
        return json.dumps(database.findCon(uid))

# delete many friends and return contact list
@app.route("/delcons/",methods=['GET','POST'])
def delcons():
    if request.method == 'POST':
        uid=session['uid']
        usrdata = json.loads(request.get_json().encode("utf-8"))
        usrlist = usrdata['id']
        for fid in usrlist:
            database.delCon(uid,fid)
        return json.dumps(database.findCon(uid))

# change nickname and return contact list [error mech]
@app.route("/setnickname/")
def setnickname():
    uid=session['uid']
    fid=request.args.get('id')
    fnickname = request.args.get('nickname')
    results = database.updateCon(uid,fid,"nickname",fnickname)
    if isinstance(results,list):
        return "error"
    else:
        return json.dumps(database.findCon(uid))

# get basic information of a invitation
@app.route("/getinv/",methods=['GET','POST'])
def getinv():
    if request.method == 'POST':
        return json.dumps(database.findInvByCreator("id,title,status",session['uid']))

# 1. get invitations that one joined 2. update user's invitation list
@app.route("/geteve/",methods=['GET','POST'])
def geteve():
    if request.method == 'POST':
        ids = json.loads(database.findUser("invitations", session['uid'])[0][0])
        flag = False
        results = []
        for iid in ids:
            t = database.findInvById("id,title,status,creator",iid)
            if len(t)==0:
                ids.remove(iid)
                flag = True
            else:
                results.append(t[0])
        if flag:
            database.updateUser('invitations',json.dumps(ids),session['uid'])
        return json.dumps(results)

# get one's contact list
@app.route("/getcon/",methods=['GET','POST'])
def getcon():
    if request.method == 'POST':
        return json.dumps(database.findCon(session['uid']))

# create invitations
@app.route("/createInvitation/",methods=['POST','GET'])
def createInvitation():
    if request.method == 'POST':
        new_inv = json.loads(request.get_json().encode("utf-8"))
        #update user data
        goal = "id,title,creator,options,startdate,description"
        data = "'"+new_inv["title"] +"'"+ "," + "'"+session["uid"]+"'" + "," +"'"+ str(new_inv["timelist"]) +"'"+ "," + "'"+cur_date[0:6] +"'"+ "," + "'"+new_inv["des"]+"'"
        #save to the database
        database.addInv(goal,data)
        return json.dumps(new_inv)

# save activity in one's calendar
@app.route("/save_activity/",methods=['POST','GET'])
def save_activity():
    new_act = json.dumps({"title":'',"start":0,"end":0})
    if request.method == 'POST':
        new_act = json.loads(request.get_json().encode("utf-8"))
        database.addTime(session['uid'], new_act["title"], calc_time(new_act["start"]), calc_time(new_act["end"]))
    return json.dumps(new_act)

# delete activity from one's calendar
@app.route("/delete_activity/",methods=['POST','GET'])
def delete_activity():
    delete_act = json.dumps({"title":'',"start":0,"end":0})
    if request.method == 'POST':
        del_act = json.loads(request.get_json().encode("utf-8"))
        database.deleteTime(session['uid'], del_act["title"], calc_time(del_act["start"]), calc_time(del_act["end"]))
    return json.dumps(del_act)

# return colors by given usrlist
@app.route("/get_color/",methods=['POST','GET'])
def get_color():
    if request.method == 'POST':
        print "in"
        print request.form['data']
        usrdata = json.loads(request.form['data'])
        usrlist = usrdata['id']
        bkdata= json.dumps(cal_color(usrlist));
        return bkdata

# return options and voters of an invitation
@app.route("/getInvOptions/",methods=['GET','POST'])
def getInvOptions():
    if request.method == 'POST':
        inv_id=request.values.get('invid')
        options=json.loads(request.values.get('opt'));
        results=[]
        for opt in options:
            l = database.findVoters(inv_id,opt)
            results.append(l)
        return json.dumps(results)

if __name__ == "__main__":
    app.run()
