from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import User 
from app import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

auth = Blueprint("auth", __name__, url_prefix="/auth")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) #User.query.get(int(user_id))古い書き方

class SignupForm(FlaskForm):
    username = StringField("ユーザー名", validators=[
        DataRequired(message="ユーザー名は必須です"),
        Length(min=3, max=20, message="ユーザー名は3文字以上20文字以内で入力してください")
    ])
    password = PasswordField("パスワード", validators=[
        DataRequired(message="パスワードは必須です"),
        Length(min=5,message="パスワードは5文字以上で設定してください")
    ])
    submit = SubmitField("登録")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if User.query.filter_by(username=username).first():
            flash("そのユーザー名は既に使われています。")
            return render_template("signup.html",form=form)

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("signup.html",form=form)

class LoginForm(FlaskForm):
    username = StringField("ユーザー名", validators=[
        DataRequired(message="ユーザー名は必須です"),
        Length(min=3, max=20, message="ユーザー名は3文字以上20文字以内で入力してください")
    ])
    password = PasswordField("パスワード", validators=[
        DataRequired(message="パスワードは必須です"),
        Length(min=5,message="パスワードは5文字以上で設定してください")
    ])
    submit = SubmitField("ログイン")
    
@auth.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("auth.mypage"))

    return render_template("login.html", form=form)

@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/mypage")
@login_required
def mypage():
    return render_template("mypage.html")
