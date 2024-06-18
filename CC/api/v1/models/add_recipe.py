from dataclasses import dataclass
from firebase_admin import auth
from ..extensions import db


@dataclass
class Add_Recipe(db.Model):
    __tablename__ = "foods"

    menu_id: int        = db.Column(db.Integer, primary_key=True)
    nama_recipes        = db.Column(db.String(50))
    image_url: str      = db.Column(db.String)
    description: str    = db.Column(db.String(100))
    ingredients: str    = db.Column(db.Text)
    instructions: str   = db.Column(db.Text)
    category: str       = db.Column(db.String(50))
    author_id: str      = db.Column(db.String, nullable=False)

