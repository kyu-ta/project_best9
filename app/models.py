from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Team(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

    players = relationship("Player", backref="team", lazy="select")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"

class Position(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

    players  = relationship("Player", backref="position", lazy="select")
    best_nine_slots = relationship("BestNineSlot", backref="position", lazy="select")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"

class Player(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("position.id"), nullable=False)

    best_nine_slots = relationship("BestNineSlot", backref="player", lazy="select")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"

class BestNine(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    best_nine_slots = relationship("BestNineSlot", backref="best_nine", lazy="select")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
    
class BestNineSlot(db.Model):
    id = Column(Integer, primary_key=True)

    position_id = Column(Integer, ForeignKey("position.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=True)
    best_nine_id = Column(Integer, ForeignKey("best_nine.id"), nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
                                                                  
class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(String())

    best_nine_id = relationship("BestNine", backref="user", lazy="select")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, username='{self.username}')>"


