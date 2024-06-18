import requests
from flask import Blueprint, request
from os import getenv
from ..extensions import db
from ..decorator import authenticated_only
from ..models.favorite_recipe import *
from ..models.dashboard import *

favorite_recipe = Blueprint("favorite_recipe", __name__)

@favorite_recipe.route("/favorite_recipe/<string:id>/favorites", methods=["POST"])
@authenticated_only
def create_favorite_recipe(id):
    reipe = db.session.get(Favorite, id)
    if not Favorite:
        return {"message": f"favorite_recipes with id {id} doesn't exist"}, 404
    
    user_id = request.user.get("uid")
    favorite_recipes = db.session.get(Favorite_Recipe, (Favorite.id, user_id))
    if favorite_recipes:
        return {"message": f"favorite_recipes {id} is already in favorites"}, 409
    
    favorite_recipes = Favorite_Recipe(Favorite_id=Favorite.id, user_id=user_id)
    db.session.add(Favorite_Recipe)
    db.session.commit()

    return {"data": Favorite.serialize(user_id)}, 200

@favorite_recipe.route("/favorite_recipe/<string:id>/favorites", methods=["DELETE"])
@authenticated_only
def delete_favorite_recipe(id):
    Favorite = db.session.get(Favorite, id)
    if not Favorite:
        return {"message": f"favorite_recipe with id {id} doesn't exist"}, 404
    
    user_id = request.user.get("uid")
    Favorite = db.session.get(favorite_recipe, (Favorite.id, user_id))
    if not favorite_recipe:
        return {"message": f"favorite_recipe {id} isn't a favorite yet"}, 409
    
    db.session.delete(favorite_recipe)
    db.session.commit()

    return {"data": Favorite.serialize(user_id)}, 200