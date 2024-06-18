from dataclasses import dataclass
from ..models.dashboard import Dashboard
from ..extensions import db
from firebase_admin import auth

@dataclass
class Favorite(db.Model):
    __tablename__ = 'favorites'

    name_recipes: str

    id: int = db.Column(db.Integer, primary_key=True)
    name_recipes: str = db.Column(db.String(100), nullable=False)
    image_url: str = db.Column(db.String, nullable=False)
    details = db.relationship("menu_details", uselist=False)
    author = db.relationship("MenuAuthor", uselist=False)

def serialize(self, user_id):
        favorite_recipe = db.session.query(favorite_recipe) \
            .filter_by(user_id=user_id, food_id=self.id).first()
        return {
            "favorite_recipe": self,
            "is_favorite": favorite_recipe != None
        }

class Favorite_Recipe(db.Model):
    __tablename__ = "favorite_recipe"

    favorites_id = db.Column(db.String(30), db.ForeignKey('favorites.id'), primary_key=True)
    user_id = db.Column(db.String, primary_key=True)

@dataclass
class MenuDetails(db.Model):
    __tablename__ = "menu_details"

    author_name: str

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.String, nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    nutritions: str = db.Column(db.Text, nullable=False)
    ingredients: str = db.Column(db.Text, nullable=False)
    instructions: str = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)

    @property
    def author_name(self):
        author = auth.get_user(uid=self.author_id)
        return author.display_name
