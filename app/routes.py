from flask import (jsonify,
                   request,
                   current_app,
                   url_for,
                   redirect,
                   render_template,
                   flash)
from flask_login import (current_user,
                         login_user,
                         logout_user,
                         login_required)

from . import app
from .users import User, LoginForm, RSVPForm


@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        u = User(form.id.data)
        if not u or not u.authenticate(form.password.data):
            flash("Invalid user id or password.")
            return(redirect(url_for("login")))
        login_user(u)
        return redirect(url_for("index"))
    else:
        return render_template("login.html.jinja", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("index.html.jinja")

@app.route("/rsvp", methods=["GET","POST"])
@login_required
def rsvp():
    form = RSVPForm()
    if request.method == "POST" and form.validate_on_submit():
        current_user.save_rsvp(form.data)
        flash("Thanks for letting us know...")
        return redirect(url_for("index"))
    form.with_data(current_user.fetch_rsvp())
    return render_template("rsvp.html.jinja", form=form)
