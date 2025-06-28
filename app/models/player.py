from sqlalchemy import Column, Integer, String, SmallInteger, Text
from sqlalchemy.orm import validates
# Local Imports
from app.database import BaseSavePlayerModel


class Player(BaseSavePlayerModel):
    __tablename__ = 'player'

    # Campos del modelo
    account_id = Column(Integer, primary_key=True)  # Equivalente a PositiveIntegerField
    name = Column(String(24))  # Equivalente a CharField(max_length=24)
    job = Column(Integer)  # Equivalente a PositiveIntegerField
    level = Column(Integer)  # Equivalente a PositiveIntegerField
    exp = Column(Integer)  # Equivalente a IntegerField
    
    def __repr__(self):
        return f"<Player(id={self.account_id}, name='{self.name}')>"


class Guild(BaseSavePlayerModel):
    __tablename__ = 'guild'  # o el nombre que prefieras para la tabla

    # Campos del modelo
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12))  # CharField(max_length=12)
    sp = Column(SmallInteger)  # SmallIntegerField
    master = Column(Integer)  # PositiveIntegerField
    level = Column(Integer, nullable=True)  # IntegerField(blank=True, null=True)
    exp = Column(Integer, nullable=True)  # IntegerField(blank=True, null=True)
    skill_point = Column(Integer)  # IntegerField
    skill = Column(Text, nullable=True)  # TextField(blank=True, null=True)
    win = Column(Integer)  # IntegerField
    draw = Column(Integer)  # IntegerField
    loss = Column(Integer)  # IntegerField
    ladder_point = Column(Integer)  # IntegerField
    gold = Column(Integer)  # IntegerField

    def __repr__(self):
        return f"<Guild(id={self.id}, name='{self.name}')>"
