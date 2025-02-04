from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)

# import bleach
import os
import enum

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, "database.db")}"
)
app.config["SECRET_KEY"] = "valentine_secret_key"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RoleEnum(enum.Enum):
    BOYFRIEND = "boyfriend"
    GIRLFRIEND = "girlfriend"


class ActivityEnum(enum.Enum):
    NAUGHTY = "naughty"
    FRIENDLY = "friendly"
    normal = "normal"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    partner = db.Column(db.Integer, db.ForeignKey("user.id"))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)


class RegisterForm(FlaskForm):
    name = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Your Name"},
    )

    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Your Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )

    role = SelectField(
        "Role",
        choices=[
            ("girlfriend", "girlfriend"),
            ("boyfriend", "boyfriend"),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError("Username already in use")


class LoginForm(FlaskForm):

    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Your Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()

        if existing_user:
            flash("User name already in use", "warning")
            return redirect(url_for("register"))
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(
                name=form.name.data,
                username=form.username.data,
                password=hashed_password,
                role=form.role.data,
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Registration Successful!")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Invalid credentials", "danger")
        else:
            flash("User not found", "warning")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in field {field}: {error}", "danger")

    return render_template("login.html", form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created!")
    app.run(debug=True, host="0.0.0.0", port=5000)
