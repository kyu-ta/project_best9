from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models import Player, Team, Position, BestNine, BestNineSlot
from app import db
from flask_login import login_required, current_user

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/players")
def players():
    players = Player.query.all()
    return render_template("players.html", players=players)

@main.route("/player/<int:id>")
def player(id):
    player = Player.query.get_or_404(id)
    return render_template("player.html", player=player)

@main.route("/teams")
def teams():
    teams = Team.query.all()
    return render_template("teams.html", teams=teams)

@main.route("/team/<int:id>")
def team(id):
    team = Team.query.get_or_404(id)
    return render_template("team.html", team=team)

@main.route("/positions")
def positions():
    positions = Position.query.all()
    return render_template("positions.html", positions=positions)

@main.route("/position/<int:id>")
def position(id):
    position = Position.query.get_or_404(id)
    players = position.players
    return render_template("position.html", position=position, players=players)

@main.route("/bestnine/create", methods=["GET", "POST"])
@login_required
def bestnine_create():
    positions = Position.query.all()

    if request.method == "POST":
        bestnine_name = request.form.get("bestnine_name")

        if not bestnine_name:
            count = BestNine.query.filter_by(user_id=current_user.id).count()
            bestnine_name = f"{current_user.username}さんのベスト9({count + 1})"
        
        new_bestnine = BestNine(name=bestnine_name,
                                user_id=current_user.id
                            )
        db.session.add(new_bestnine)
        db.session.flush()
        
        for position in positions:
            #player_id = request.form.get(f"player_{ position.id }")↓と同じだが、変数にしてわかりやすくしている

            player_key = f"player_{ position.id }"    #print(player_key)などでキーを確認できる
            player_id = request.form.get(player_key)

            new_bestnine_slot = BestNineSlot(
                best_nine_id=new_bestnine.id, 
                player_id=player_id, 
                position_id=position.id
            )     
                        
            db.session.add(new_bestnine_slot)
        db.session.commit()
        flash("保存しました")
        return redirect(url_for("auth.mypage"))

    return render_template("bestnine_create.html", positions=positions)

@main.route("/bestnine/<int:id>")
@login_required
def bestnine_detail(id):
    bestnine = BestNine.query.get_or_404(id)    
    return render_template("bestnine_detail.html", bestnine=bestnine)

@main.route("/bestnine/delete/<int:id>", methods=["POST"])
@login_required
def bestnine_delete(id):
    bestnine = BestNine.query.get_or_404(id)
    db.session.delete(bestnine)
    db.session.commit()
    flash("ベスト9を削除しました")

    return redirect(url_for("auth.mypage"))