from flask import Blueprint
from .routes import dashboard, add_recipe, favorite_recipe, profiles,auth,search

v1 = Blueprint("v1", __name__)
v1.register_blueprint(dashboard.dashboard)
v1.register_blueprint(add_recipe.add_recipe)
v1.register_blueprint(favorite_recipe.favorite_recipe)
v1.register_blueprint(profiles.profile)
v1.register_blueprint(auth.auth)
v1.register_blueprint(search.search)