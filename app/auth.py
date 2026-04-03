from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__, url_prefix="/auth")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) #User.query.get(int(user_id))古い書き方

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("auth.mypage"))
        else:
            flash("ログイン失敗")
    
    return render_template("login.html")

@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("ユーザー名とパスワードは必須です。")
            return render_template("signup.html")
        
        if User.query.filter_by(username=username).first():
            flash("そのユーザー名は既に使われています。")
            return render_template("signup.html")
        
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("ユーザー登録完了。ログインしてください。")
        return redirect(url_for("auth.login"))


    return render_template("signup.html")
        

@auth.route("/mypage")
@login_required
def mypage():
    return render_template("mypage.html")
