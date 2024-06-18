import requests
from flask import Blueprint, request
from os import getenv
from ..extensions import db
from ..decorator import authenticated_only
from ..models.dashboard import *

search = Blueprint("search", __name__)

@search.route("/food-categories", methods=["GET"])
@authenticated_only
def get_food_categories():
    categories = db.session.query(MenuCategory) \
        .order_by(MenuCategory.name.asc()).all()
    return {"data": categories}, 200

@search.route("/food-recommendations", methods=["GET"])
@authenticated_only
def get_food_recomendations():
    user_id = request.user.get("uid")
    url = getenv("RECOMMENDATIONS_SERVICE")

    response = requests.post(f"{url}/predict", json={"user_id": user_id})
    if response.status_code == 200:
        Dashboard = list()
        for item in response.json().get("data"):
            Dashboard = db.session.get(Dashboard, list(item))
            if Dashboard:
                Dashboard.append(Dashboard)
        return {"data": Dashboard.serialize_list(user_id, Dashboard)}, 200
    return {"data": []}, 200