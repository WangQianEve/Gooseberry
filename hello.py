from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome To Gooseberry!"

@app.route("/index/")
def index():
    return render_template("index.html")

@app.route("/user/")
def user():
    return render_template("user.html")

@app.route("/invitation/<inv_id>")
def invitation(inv_id):
    if(True):
        return render_template("invitation.html")
    else:
        return "Invitation does not exist!"
		
@app.route("/timetable/")
def timetable():
    return render_template("timetable_test.html")
	
@app.route("/tablesuperimposition/")
def tablesuperimposition():
    return render_template("table_superimposition.html")	

if __name__ == "__main__":
    app.run()
