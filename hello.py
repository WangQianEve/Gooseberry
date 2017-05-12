from flask import Flask
from flask import abort, redirect, url_for
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/index/")
def index():
    if not signed-in:
        return redirect(url_for('hello'))
    else:
        get invitation list
        get join list
        get 
        return render_template("index.html")

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
            return render_template("invitation.html")
        else:
            return "Invitation does not exist!"

if __name__ == "__main__":
    app.run()
