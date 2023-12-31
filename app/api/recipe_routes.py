from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import Recipe, Review
from app.forms import RecipeForm
from app.forms import ReviewForm
from app import db

recipe_routes = Blueprint('recipes', __name__)

@recipe_routes.route("")
def get_recipe():
  recipes = Recipe.query.all()
  return {"recipes": [recipe.to_dict() for recipe in recipes]}

@recipe_routes.route("/<int:id>")
def get_recipe_detail(id):
  recipe = Recipe.query.get(id)

  if not recipe:
    return {"error": "cannot find recipe"}

  return {'recipe': recipe.to_dict_detailed()}

@recipe_routes.route("/<int:id>", methods=['PUT'])
def update_recipe(id):
  form = RecipeForm()
  recipe = Recipe.query.get(id)

  form['csrf_token'].data = request.cookies['csrf_token']

  print(form.data)

  if form.validate_on_submit():
    print("INSIDE FORM VALIDATION BLOCK")
    print(recipe.name)
    recipe.name = form.data["name"]
    print(recipe.name)
    recipe.description = form.data["description"]
    recipe.instruction = form.data["instruction"]
    recipe.cover_image = form.data["cover_image"]
    recipe.ingredient_list = form.data["ingredient_list"]
    db.session.commit()
    return {"recipe": recipe.to_dict()}
  return {"errors": form.errors}, 400



@recipe_routes.route("/new", methods=["POST"])
def new_recipe():
  form = RecipeForm()

  form['csrf_token'].data = request.cookies['csrf_token']

  print(form.data)

  if form.validate_on_submit():
    recipe = Recipe(
      owner_id=form.data["owner_id"],
      name=form.data["name"],
      ingredient_list=form.data["ingredient_list"],
      description=form.data["description"],
      cover_image=form.data["cover_image"],
      instruction=form.data["instruction"]
    )
    db.session.add(recipe)
    db.session.commit()
    return {'recipe': recipe.to_dict()}
  return {"errors": form.errors}, 400

@recipe_routes.route('/<int:recipeId>/new', methods=["POST"])
def add_review(recipeId):
  recipe = Recipe.query.get(recipeId)

  form = ReviewForm()

  form['csrf_token'].data = request.cookies['csrf_token']

  if form.validate_on_submit():
    print(form.data, recipe)
    review = Review(
      user_id=form.data["user_id"],
      recipe_id=form.data["recipe_id"],
      star_rating=form.data["star_rating"],
      comment=form.data["comment"]
    )
    db.session.add(review)
    db.session.commit()
    return {'recipe': recipe.to_dict_detailed()}

  else:
    return {"error": "Could not find recipe"}

@recipe_routes.route("/<int:id>", methods=["DELETE"])
def delete_recipe(id):
  recipe = Recipe.query.get(id)
  db.session.delete(recipe)
  db.session.commit()
  return {"message": "post deleted"}
