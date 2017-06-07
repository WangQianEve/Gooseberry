from flask import Flask
from flask import abort, redirect, url_for, render_template
from flask import request, session
import database
import json
from flask import jsonify
from data import timeunit,timetable,activity,user
import time,datetime

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = '|G\x8f\x7f\x02\xb87\x9cYai\xc4D\x11\xd4\xf4j>\x1a\x15\xdc\x95l\x1f'


def update_user_calendar(usr,time_unit_list):
    usr.user_week_time_table.clear_timetable()
    for i in time_unit_list:
        usr.user_week_time_table.add_time_unit(cur_date,i,1,'default')

#Make some data to use
lineNum = 24
time_amount = 7*lineNum
cur_date = time.strftime('%y%m%d0000',time.localtime(time.time()))
user1 = user(001)
user2 = user(002)
user3 = user(003)
cur_user = ''
total_user = [user1,user2,user3]
default_bkdata = {"color1":[],"color2":[],"color3":[5,17,25,64,100]}

user1.friendlist.append(user2)
user1.friendlist.append(user3)
list1=[5,17,25,64,100]
list2=[5,22,64,80]
list3=[5,20,25,90]

update_user_calendar(user1,list1)
update_user_calendar(user2,list2)
update_user_calendar(user3,list3)


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
            usrlist = [session['uid']]
            bkdata= json.dumps(cal_color(usrlist))
            print "bkdata"
            print bkdata
            return render_template("index.html", uname=session['username'],bgcolor = bkdata,table_data=table_data,friendlist = friendlist)
        else:
            return render_template("hello.html", msg="User ID or Password wrong!")
    if 'uid' in session:
        
        table_data = json.dumps(get_table_info_by_usr(session['uid']))
        friendlist = database.findCon(session['uid'])
        usrlist = [[session['uid']]]
        bkdata= json.dumps(cal_color(usrlist));
        print "bkdata"
        print bkdata
        return render_template("index.html", uname=session['username'],bgcolor = bkdata,table_data=table_data,friendlist = friendlist)
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
        searchText = request.values.get('ids').split(';');
        uid=session['uid']
        frList=[]
        nofrList=[]
        noPerList=[]
        for fid in searchText:
            t = database.relation(uid,fid.strip())
            print(t)
            if len(t)>0:
                frList.append(t[0])
            else:
                print(t)
                t = database.findUser("id,name",fid)
                if len(t)>0:
                    nofrList.append(t[0])
                else:
                    noPerList.append(fid)
        result = {}
        result['friends']=frList
        result['strangers']=nofrList
        result['wrong']=noPerList
        print result
        return json.dumps(result)

@app.route("/addcon/")
def addcon():
    uid=session['uid']
    fid=request.args.get('id')
    fname=request.args.get('name')
    database.addCon(uid,fid,fname,"")
    return "success"

@app.route("/delcon/",methods=['GET','POST'])
def delcon():
    if request.method == 'POST':
        uid=session['uid']
        print request.get_json()
        usrdata = json.loads(request.get_json().encode("utf-8"))
        usrlist = usrdata['id']
        for fid in usrlist:
            
            database.delCon(uid,fid)
        data = database.findCon(session['uid'])
        #data = {"id":[]}
        #for i in list:
        #    data["id"].append(i[0])
        #data = json.dumps(data)
        print "friendlist"
        print data
        return json.dumps(data)
    else:
        uid=session['uid']
        fid=request.args.get('id')
        database.delCon(uid,fid)
        print "success"
        return "success"

@app.route("/setnickname/")
def setnickname():
    uid=session['uid']
    fid=request.args.get('id')
    fnickname = request.args.get('nickname')
    results = database.updateCon(uid,fid,"nickname",fnickname)
    if isinstance(results,(list)):
        return "error"
    else:
        return "success"

@app.route("/getinv/",methods=['GET','POST'])
def getinv():
    if request.method == 'POST':
        return json.dumps(database.findInvByCreator("iid,ititle,istate,icount",session['uid']))

@app.route("/geteve/",methods=['GET','POST'])
def geteve():
    if request.method == 'POST':
        ids = json.loads(database.findUser("invitations", session['uid'])[0][0])
        print ids
        flag = False
        results = []
        for iid in ids:
            t = database.findInvById("id,title,state,count,creator",iid)
            if len(t)==0:
                ids.remove(iid)
                flag = True
            else:
                results.append(t[0])
        if flag:
            database.updateUser('invitations',json.dumps(ids),session['uid'])
        return json.dumps(results)

@app.route("/joinInv/")
def joinInv():
    invId = request.args.get('inv')
    uid = session['uid']
    database.invAddMember(invId,uid)
    database.userAddInv(invId,uid)


@app.route("/getcon/",methods=['GET','POST'])
def getcon():
    if request.method == 'POST':
        return json.dumps(database.findCon(session['uid']))
        #return json.dumps({"data":"getcon"})

def count_time_unit(t):
    time_num = 0
    print " count time unit "
    d1 = datetime.datetime(int('20'+t[0:2]), int(t[2:4]), int(t[4:6]))
    d2 = datetime.datetime(int('20'+cur_date[0:2]), int(cur_date[2:4]), int(cur_date[4:6]))
    time_num = (d1-d2).days * lineNum + int(t[6:8])*lineNum/24 
    print time_num
    return time_num
    
def calc_time(time_num):
    t = 0
    print " month "
    print int(cur_date[2:4])
    print cur_date
    d1 = datetime.datetime(int('20'+cur_date[0:2]), int(cur_date[2:4]), int(cur_date[4:6]))
    d2 = (d1 + datetime.timedelta(days=time_num/lineNum)).strftime('%y%m%d')  
    t = d2 + '%02d' %(time_num % lineNum) + '00' 
    return t

def get_table_info_by_usr(usr):
    table_data = {"time" : []}
    if 'uid' in session:
        user_data = database.findTime(usr,cur_date)
        print "user data"
        print user_data
        for i in user_data:
            start_time = i[1].strftime('%y%m%d%H00')
            start_num = count_time_unit(start_time)
            end_time = i[2].strftime('%y%m%d%H00')
            end_num = count_time_unit(end_time)
            act = {"title":i[0],"start":start_num,"end":end_num}
            table_data["time"].append(act)
    print "table data "    
    print table_data

    return table_data

def find_user_by_id(id):
    for i in total_user:
        if(i.id == id):
            return i
    return None

def cal_color(usrlist):
    color_data ={"color1":[],"color2":[],"color3":[]}
    tmpdict={}
    #Count the times of each time unit
    #get users'data from database
    for u in usrlist:
        user_data = database.findTime(u,cur_date)
        for i in user_data:
            start_time = i[1].strftime('%y%m%d%H00')
            start_num = count_time_unit(start_time)
            end_time = i[2].strftime('%y%m%d%H00')
            end_num = count_time_unit(end_time)

            for k in range(start_num, end_num + 1):
                if not str(k) in tmpdict:
                    tmpdict[str(k)] = 1
                else:
                    tmpdict[str(k)] += 1

    for key in tmpdict:
        #print 'key: '+key+'  '+str(tmpdict[key])
        if tmpdict[key] == 1:
            color_data["color1"].append(int(key))
        elif tmpdict[key] == 2:
            color_data["color2"].append(int(key))
        else:
            color_data["color3"].append(int(key))
    return color_data


# evoked by user.html
@app.route("/createInvitation/",methods=['POST','GET'])
def createInvitation():
		#new_inv = json.dumps({"title":'',"start":0,"end":0})
        if request.method == 'POST':
            new_inv = json.loads(request.get_json().encode("utf-8"))
            print "new inv!!"
            print new_inv
            #update user data
            goal = "id,title,creator,options,startdate,discription"
            data = "'"+new_inv["title"] +"'"+ "," + "'"+session["uid"]+"'" + "," +"'"+ str(new_inv["timelist"]) +"'"+ "," + "'"+cur_date[0:6] +"'"+ "," + "'"+new_inv["des"]+"'"
            #save to the database
            print goal
            print data
            database.addInv(goal,data)
        return json.dumps(new_inv)

@app.route("/save_time/",methods=['POST','GET'])
def save_time():
        if request.method == 'POST':
            data = json.loads(request.get_json().encode("utf-8"))
            default_bkdata['color3']=data['id']
            #save to the user
            update_user_calendar(cur_user,default_bkdata['color3'])
        bkdata= json.dumps(default_bkdata);
        return bkdata

@app.route("/save_activity/",methods=['POST','GET'])
def save_activity():
        new_act = json.dumps({"title":'',"start":0,"end":0})
        if request.method == 'POST':
            new_act = json.loads(request.get_json().encode("utf-8"))
            print "new act!!"
            print new_act
            #update user data

            #save to the database
            
            database.addTime(session['uid'], new_act["title"], calc_time(new_act["start"]), calc_time(new_act["end"]))
        return json.dumps(new_act)

@app.route("/delete_activity/",methods=['POST','GET'])
def delete_activity():
        delete_act = json.dumps({"title":'',"start":0,"end":0})
        if request.method == 'POST':
            del_act = json.loads(request.get_json().encode("utf-8"))
            print "del act!!"
            print del_act
            #update user data

            #save to the database
            database.deleteTime(session['uid'], del_act["title"], calc_time(del_act["start"]), calc_time(del_act["end"]))
        return json.dumps(del_act)

@app.route("/get_color/",methods=['POST','GET'])
def get_color():
        usrlist = [session['uid']]
        if request.method == 'POST':
            #usrdata = request.get_json()
            usrdata = json.loads(request.get_json().encode("utf-8"))
            usrlist = usrdata['id']
            
            usrlist.append(session['uid'])

        print usrlist
        bkdata= json.dumps(cal_color(usrlist));
        print bkdata
        return bkdata

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

@app.route("/timetable", methods=['POST','GET'])
def timetable():
    if request.method == 'POST':
        data = request.get_json()
    else:
        data = {}
    return render_template("timetable_test.html",data=data)

@app.route("/tablesuperimposition/")
def tablesuperimposition():
    return render_template("table_superimposition.html")




if __name__ == "__main__":
    app.run()
