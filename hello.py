from flask import Flask
from flask import abort, redirect, url_for, render_template
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/index/")
def index():
        user = 001
    # if not signed-in:
    #     return redirect(url_for('hello'))
    # else:
    #     get user
        return render_template("index.html", user=user)

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

@app.route("/user/")
def user():
    # if not signed-in:
    #     return redirect(url_for('hello'))
    # else:
        return render_template("user.html")

@app.route("/invitation/<inv_id>")
def invitation(inv_id):
    invitation = 'inv'
    return render_template("invitation.html", data=invitation, on_create = on_create)
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

if __name__ == "__main__":
    app.run()
