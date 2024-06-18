from dataclasses import dataclass
from firebase_admin import auth
from ..extensions import db

@dataclass
class Dashboard(db.Model):
    __tablename__ = "dashboards"

    name_recipes: str
    category_name: str
    rating: str

    id: int = db.Column(db.Integer, primary_key=True)
    name_recipes: str = db.Column(db.String(100), nullable=False)
    image_url: str = db.Column(db.String, nullable=False)
    category_id: int = db.Column(db.Integer, db.ForeignKey('campaign_categories.id'), nullable=False)
    details = db.relationship("menu_details", uselist=False)
    author = db.relationship("MenuAuthor", uselist=False)

    @property
    def category_name(self):
        return db.session.get(MenuCategory, self.category_id).name
    
@dataclass
class MenuDetails(db.Model):
    __tablename__ = "menu_details"

    author_name: str

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.String, nullable=False)
    name_recipes: str = db.Column(db.String(100), nullable=False)
    image_url: str = db.Column(db.String, nullable=False)
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

@dataclass
class MenuCategory(db.Model):
    __tablename__ = "menu_categories"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), unique=True, nullable=False)

@dataclass
class MenuFavorite(db.Model):
    __tablename__ = "menu_favorites"
    
    menu_id = db.Column(db.String(30), db.ForeignKey('dashboards.id'), primary_key=True)
    user_id = db.Column(db.String, primary_key=True)
