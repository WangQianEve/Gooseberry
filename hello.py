from flask import Flask
from flask import abort, redirect, url_for
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/index/")
def index():
    if not signed-in:
        return redirect(url_for('hello'))
    else:
        get user
        return render_template("index.html", user=user)

@app.route("/createInvitation/")
def createInvitation():
    id=002
    if success:
        return redirect(url_for('invitation', inv_id=id, on_create=True ))
    else:
        return 0

@app.route("/user/")
def user():
    if not signed-in:
        return redirect(url_for('hello'))
    else:
        return render_template("user.html")

@app.route("/invitation/<inv_id>")
def invitation(inv_id):
    if not signed-in:
        return redirect(url_for('hello'))
    else:
        if id valid:
            get invitation
            return render_template("invitation.html", data=invitation, on_create = on_create)
        else:
            return "Invitation does not exist!"

if __name__ == "__main__":
    app.run()
