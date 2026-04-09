from app import db
from datetime import datetime, UTC
from zoneinfo import ZoneInfo
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Team(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    players = relationship("Player", backref="team", lazy="select")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"

class Position(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

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
    created_at = Column(DateTime, default=lambda:datetime.now(UTC).replace(tzinfo=None), nullable=False)
    
    @property
    def created_at_jst(self):
        if self.created_at is None:
            return None
        if self.created_at.tzinfo is None:
            utc_dt = self.created_at.replace(tzinfo=UTC)
        else:
            utc_dt = self.created_at
        return utc_dt.astimezone(ZoneInfo("Asia/Tokyo"))
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    best_nine_slots = relationship("BestNineSlot",
                                    backref="best_nine",
                                    cascade="all, delete-orphan",#orphan-孤児
                                    lazy="select"
                                )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
    
class BestNineSlot(db.Model):
    id = Column(Integer, primary_key=True)

    position_id = Column(Integer, ForeignKey("position.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=True)
    best_nine_id = Column(Integer, ForeignKey("best_nine.id"), nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
                                                                  
class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    best_nines = relationship("BestNine", backref="user", lazy="select")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, username='{self.username}')>"


