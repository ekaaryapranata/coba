from datetime import date
from firebase_admin import auth
from flask import Blueprint, request
from ..extensions import db
from ..decorator import authenticated_only
from ..models.dashboard import *

dashboard = Blueprint("dashboards", __name__)

@dashboard.route("/dashboard/<int:id>/details", methods=["GET"])
@authenticated_only
def get_menu_detail(id):
    menu_detail = db.session.query(MenuDetails) \
        .filter_by(menu_id=id).first()
    if not menu_detail:
        return {"message": f"Menu with id {id} doesn't exist"}, 404
    
    user_id = request.user.get("uid")
    return {"data": menu_detail.serialize(user_id, id)}, 200

@dashboard.route("/menu-categories", methods=["GET"])
def get_menu_categories():
    categories = db.session.query(MenuCategory) \
        .order_by(MenuCategory.name.asc()).all()
    return {"data": categories}, 200

@dashboard.route("/dashboard/<string:id>/favorites", methods=["POST"])
@authenticated_only
def create_menu_favorite(id):
    
    user_id = request.user.get("uid")
    menu_favorites = db.session.get(MenuFavorite, (menu_favorites.id, user_id))
    if menu_favorites:
        return {"message": f"This menu {id} is already in favorites"}, 409
    
    menu_favorites = MenuFavorite(menu_favorites_id=menu_favorites.id, user_id=user_id)
    db.session.add(menu_favorites)
    db.session.commit()

    return {"data": menu_favorites.serialize(user_id)}, 200
