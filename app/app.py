from flask import Flask, render_template, make_response, request, redirect
from flask_login import current_user, login_required, logout_user
from flask_wtf.csrf import CSRFProtect
from auth import register, login_manager, login, get_user
from db import db
from event import get_events, get_event, get_participants, join_event, new_event

app = Flask(__name__)
app.secret_key = "d6cf28f632b5e1b52e476817a306446154841aea065217409a7e136d0b73a0f7277181c7a18afad7cf67e2e8b9ddf9341073034c039f17ad61cbcd227123259f"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"


csrf = CSRFProtect(app)
db.init_app(app)
login_manager.init_app(app)
with app.app_context():
    db.create_all()


@app.template_filter()
def pretty_time(time):
    return time.strftime("%H:%M:%S")


@app.template_filter()
def pretty_time2(time):
    return str(time).rjust(2, "0")


@app.template_filter()
def event_user(event):
    user = get_user(event.creator, True)
    return user.username


@app.route("/")
@login_required
def index():
    return make_response(redirect("/event"))


@app.route("/event")
@login_required
def events():
    if request.method == "GET" and "creator" in request.args.keys():
        events = get_events(request.args["creator"])
    else:
        events = get_events()
    return make_response(render_template("index.html", events=events))


@app.route("/event/<id>")
@login_required
def event_id(id):
    event = get_event(id)
    if event is None:
        return make_response(redirect("/event"))
    participants = get_participants(event)
    return make_response(render_template("event.html", event=event, participants=participants))


@app.route("/event/<id>/join")
@login_required
def event_join(id):
    join_event(id, current_user.id)
    return make_response(redirect(f"/event/{id}"))


@app.route("/event/new", methods=["GET", "POST"])
@login_required
def event_create():
    if request.method == "POST":
        result = new_event(request.form)
        return make_response(redirect("/event"))
    return make_response(render_template("new_event.html"))


@app.route("/register", methods=["GET", "POST"])
def request_register():
    if current_user.is_authenticated:
        return make_response(redirect("/"))
    if request.method == "POST":
        resp = register(request.form, db)
    else:
        resp = render_template("register.html")
    return make_response(resp)


@app.route("/login", methods=["GET", "POST"])
def request_login():
    if request.method == "GET":
        return make_response(render_template("login.html"))
    if login():
        resp = redirect("/")
    else:
        resp = render_template('login.html', errors=[
                               "Wrong password or Login Id not exists"])
    return make_response(resp)


@app.route("/logout")
@login_required
def request_logout():
    logout_user()
    return make_response(redirect("/login"))


if __name__ == "__main__":
    app.run(debug=True, port=5555)
