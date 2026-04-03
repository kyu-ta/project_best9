import csv
from app import create_app, db
from app.models import Player, Team, Position

app = create_app()#アプリファクトリで作ったcreate_app関数を使ってアプリを作る。モデル定義などもされている

with app.app_context():#appの中身をapp_context()メソッドで今から使うアプリとして紐づける→with文で開き、終わったら閉じる。
    Player.query.delete()

    with open("players.csv", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for player_data in reader:
            team = Team.query.filter_by(name=player_data["team"]).first()
            position = Position.query.filter_by(name=player_data["position"]).first()

            if team is None:
                print(f"チームが見つからない: {player_data['team']}")
                continue

            if position is None:
                print(f"ポジションが見つからない: {player_data['position']}")
                continue

            player = Player(
                name = player_data["name"],
                team = team,
                position = position
            )
            db.session.add(player)
        db.session.commit()
    print("インポート完了")