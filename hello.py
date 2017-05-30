from flask import Flask
from flask import abort, redirect, url_for, render_template
from flask import request
from flask import jsonify
import json
from data import timeunit,timetable,activity,user
app = Flask(__name__)


def update_user_calendar(usr,time_unit_list):
    usr.user_week_time_table.clear_timetable()
    for i in time_unit_list:
        usr.user_week_time_table.add_time_unit(cur_date,i,1)

#Make some data to use
time_amount = 7*36
cur_date = 20170101
user1 = user(001)
user2 = user(002)
user3 = user(003)
cur_user = user1
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


def find_user_by_id(id):
    for i in total_user:
        if(i.id == id):
            return i
    return None

def cal_color(usrlist):
    color_data ={"color1":[],"color2":[],"color3":[]}
    tmpdict={}
	#Count the times of each time unit
    for i in usrlist:
        usr = find_user_by_id(int(i))
        #usr.user_week_time_table.print_timetable()
        for k in usr.user_week_time_table.week_table:
            if not str(k.get_number()) in tmpdict:
                tmpdict[str(k.get_number())] = 1
            else:
                tmpdict[str(k.get_number())] += 1

    for key in tmpdict:
        #print 'key: '+key+'  '+str(tmpdict[key])
        if tmpdict[key] == 1:
            color_data["color1"].append(int(key))
        elif tmpdict[key] == 2:
            color_data["color2"].append(int(key))
        else:
            color_data["color3"].append(int(key))
    return color_data



@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/index/",methods=['POST','GET'])
def index():
        user = 001
       
        if request.method == 'POST':
            data = json.loads(request.get_json().encode("utf-8"))
            default_bkdata['color3']=data['id']
		
        bkdata= json.dumps(default_bkdata);
        print bkdata
    # if not signed-in:
    #     return redirect(url_for('hello'))
    # else:
    #     get user
        return render_template("index.html", user=user, bgcolor = bkdata)

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

@app.route("/user/",methods=['POST','GET'])
def user():
    # if not signed-in:
    #     return redirect(url_for('hello'))
    # else:
        usrlist = [cur_user.id]
        if request.method == 'POST':
            usrdata = json.loads(request.get_json().encode("utf-8"))
            usrlist = usrdata['id']
            usrlist.append(cur_user.id)
        
        print usrlist
        bkdata= json.dumps(cal_color(usrlist));
        print bkdata
        return render_template("user.html",bgcolor = bkdata,friendlist=cur_user.friendlist)

@app.route("/get_color/",methods=['POST','GET'])
def get_color():
        usrlist = [cur_user.id]
        if request.method == 'POST':
            print type(request.get_json())
            #usrdata = request.get_json()
            usrdata = json.loads(request.get_json().encode("utf-8"))
            usrlist = usrdata['id']
            usrlist.append(cur_user.id)
        
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
