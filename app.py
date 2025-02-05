from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired

# from flask_uploads import UploadSet, configure_uploads, IMAGES
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
import cloudinary
import cloudinary.api
import cloudinary.uploader

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, "database.db")}"
)
app.config["SECRET_KEY"] = "valentine_secret_key"
app.config["UPLOADED_IMAGES_DEST"] = (
    "static/uploads"  # Save images inside "static/uploads"
)

# images = UploadSet("images", IMAGES)
# configure_uploads(app, images)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

cloudinary.config(
    cloud_name="dn0oyklzh",
    api_key="885238954191491",
    api_secret="E-PHLOY6Q6z2Hf9MqD0Ea36Xz5c",
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RoleEnum(enum.Enum):
    BOYFRIEND = "BOYFRIEND"
    GIRLFRIEND = "GIRLFRIEND"


class ActivityEnum(enum.Enum):
    NAUGHTY = "NAUGHTY"
    FRIENDLY = "FRIENDLY"
    NORMAL = "NORMAL"


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    liked_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", foreign_keys=[user_id])
    liked_user = db.relationship("User", foreign_keys=[liked_user_id])

    def __repr__(self):
        return f"<Like {self.user_id} -> {self.liked_user_id}>"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    partner = db.Column(db.Integer, db.ForeignKey("user.id"))
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    taken = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(255), nullable=True)
    likes = db.Column(db.Integer, default=0)

    # Rename the backref to avoid name conflicts
    liked_users = db.relationship(
        "Like", backref="user_who_likes", lazy="dynamic", foreign_keys=[Like.user_id]
    )
    liked_by_users = db.relationship(
        "Like",
        backref="user_who_is_liked",
        lazy="dynamic",
        foreign_keys=[Like.liked_user_id],
    )


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
            ("BOYFRIEND", "BOYFRIEND"),
            ("GIRLFRIEND", "GIRLFRIEND"),
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


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    user = current_user
    search_query = request.args.get("search", "")
    image_url = None

    users = []
    if search_query:
        users = User.query.filter(User.username.ilike(f"%{search_query}")).all()

    return render_template(
        "home.html",
        user=user,
        users=users,
        search_query=search_query,
        image_url=image_url,
    )


@app.route("/upload_image", methods=["POST"])
@login_required
def upload_image():
    if "image" in request.files:
        image_file = request.files["image"]
        if image_file:
            # 🔹 Upload Image to Cloudinary
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result["secure_url"]  # Get Cloudinary URL

            # 🔹 Store the image URL in the user's profile
            current_user.image_url = image_url
            db.session.commit()

            flash("Image uploaded successfully!", "success")
            return redirect(url_for("home"))

    flash("No image selected", "warning")
    return redirect(url_for("home"))


@app.route("/like-user/<int:user_id>", methods=["POST", "GET"])
@login_required
def like_user(user_id):
    liked_user = User.query.get(user_id)

    if not liked_user:
        return redirect(url_for("home"))

    if liked_user.id == current_user.id:
        return redirect(url_for("home"))

    existing_like = Like.query.filter_by(
        user_id=current_user.id, liked_user_id=liked_user.id
    ).first()

    if existing_like:
        db.session.delete(existing_like)
        liked_user.likes -= 1
        db.session.commit()
    else:
        new_like = Like(user_id=current_user.id, liked_user_id=liked_user.id)
        db.session.add(new_like)
        liked_user.likes += 1
        db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created!")
    app.run(debug=True, host="0.0.0.0", port=5000)
