from firebase_admin import auth
from flask import Blueprint, request
from os import getenv
from ..extensions import db
from ..decorator import authenticated_only
from ..helper import get_bucket_storage
from ..models.dashboard import Dashboard
from ..models.add_recipe import *

add_recipe = Blueprint("add_recipe", __name__)

@add_recipe.route("/add_recipe", methods = ['POST'])
@authenticated_only
def create_recipe():
    data = request.form if request.content_type.startswith("multipart/form-data") else request.json

    name_recipes    = data.get("name_recipes")
    description     = data.get("description")
    ingredients     = data.get("ingredients")
    instructions    = data.get("instructions")
    category        = data.get("category")

    if not name_recipes or not description or not ingredients or not instructions or not description or not category:
        return {"message": "Name menu,description,ingredients,instructions,category are required"}, 400
    
    image = request.files.get("image")
    image_url = None
    
    if image:
        if not image.content_type.startswith("image/"):
            return {"message": "File is not a valid image"}, 400
        
        bucket = get_bucket_storage(getenv("BUCKET_NAME"))
        blob = bucket.blob(f"add_recipe/{image.filename}")

        blob.upload_from_file(image)
        blob.make_public()
        image_url = blob.public_url

    add_recipe = Add_Recipe( nama_recipes = name_recipes ,image_url= image_url , description= description, ingredients= ingredients,instructions= instructions,category= category, author_id=request.user.get('user_id'))
    db.session.add(add_recipe)
    db.session.commit()