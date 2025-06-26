from sqlalchemy import Column, Integer, String, Text, SmallInteger
# Local Imports
from app.database import BaseSavePlayerModel


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
