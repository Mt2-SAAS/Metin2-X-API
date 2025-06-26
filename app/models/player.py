from sqlalchemy import Column, Integer, String, Index
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
