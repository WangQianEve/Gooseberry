from flask import Flask
from flask import abort, redirect, url_for, render_template
from flask import request
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/index/")
def index():
        user = 001
        bkdata= json.dumps({"color1":[5,17,25],"color2":[50,200],"color3":[64,21]});
        		
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

@app.route("/user")
def user():
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
