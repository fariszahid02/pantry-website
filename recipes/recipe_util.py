# Authored by: Faris, Joe, Yat Nam, Keirav
# utility functions for recipe management
from flask_login import current_user

from extensions import db
from models import Recipe, Ingredient, Rating, create_and_get_qfid, \
    create_or_get_food_item, ShoppingList, InUseRecipe, User
from shopping.shopping_util import create_shopping_item, create_shopping_list_util


def create_recipe(name, method, serving_size, calories, ingredients):
    new_recipe = Recipe(user_id=current_user.id,
                        recipe_name=name,
                        cooking_method=method,
                        serves=serving_size,
                        calories=calories)
    db.session.add(new_recipe)
    db.session.commit()
    recipe_id = new_recipe.id
    for ingredient in ingredients:
        add_ingredient(ingredient["food"], ingredient["quantity"], ingredient["unit"], new_recipe.id)


def add_ingredient(ingredient, quantity, unit, recipe_id):
    food_id = create_or_get_food_item(ingredient).id
    qfid = create_and_get_qfid(food_id, quantity, unit)
    new_ingredient = Ingredient(recipe_id=recipe_id,
                                qfood_id=qfid)
    db.session.add(new_ingredient)
    db.session.commit()


def get_pantry_dict(user_pantry):
    """
    Utility function to create a dictionary of pantry items with their quantities from My Pantry.
    """
    pantry_dict = {}
    for item in user_pantry:
        if item.get_name() not in pantry_dict:
            pantry_dict[item.get_name()] = 0
        pantry_dict[item.get_name()] += item.get_quantity()
    return pantry_dict


def check_recipe_ingredients(ingredients, pantry_dict):
    """
    Utility function to check if the user can make a recipe with their pantry items and identify missing ingredients.
    """
    can_make_recipe = True
    missing_ingredients = []
    for ingredient in ingredients:
        qfi_ingredient = ingredient.qfooditem
        ingredient_name = ingredient.get_name()
        ingredient_quantity = ingredient.get_quantity()

        if ingredient_name not in pantry_dict or pantry_dict[ingredient_name] < ingredient_quantity:
            can_make_recipe = False
            missing_quantity = ingredient_quantity - pantry_dict.get(ingredient_name, 0)
            missing_ingredients.append({
                'name': ingredient_name,
                'quantity': missing_quantity,
                'units': qfi_ingredient.units
            })
    return can_make_recipe, missing_ingredients


def update_recipe_rating(recipe_id):
    recipe: Recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe:
        recipe.update_rating()


# Method to rate a recipe. Takes user, recipe and numeric value of rating as parameters.
# Recipe's rating value is updated as well.
def create_recipe_rating(user_id: int, recipe_id: int, rating: int) -> None:
    rating = Rating(user_id=user_id, recipe_id=recipe_id, rating=rating)
    db.session.add(rating)
    db.session.flush()
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    recipe.update_rating()


# Method to delete an instance of a recipe. First all Qfooditems related to the recipe's ingredients are removed.
# All ingredients and ratings which are related to the given recipe are deleted automatically db cascading.
# Takes recipe object to be deleted as parameter.
def delete_recipe_instance(recipe: Recipe) -> None:
    qfoods = [ingredient.qfooditem for ingredient in recipe.ingredients]
    for qfood in qfoods:
        db.session.delete(qfood)
    db.session.delete(recipe)
    db.session.commit()


def save_rating(user_id, recipe_id, rating):
    recipe: Recipe = Recipe.query.filter_by(id=recipe_id).first()
    existing_rating = Rating.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing_rating:
        existing_rating.set_rating(rating)
        recipe.update_rating()
    else:
        create_recipe_rating(user_id=user_id, recipe_id=recipe_id, rating=rating)
    db.session.commit()


def get_in_use_recipes(user_id):
    # This function should return a list of recipes in use by the user
    # For demonstration purposes, let's assume we return all recipes
    return Recipe.query.filter_by(user_id=user_id).all()


def complete_and_rate_recipe(recipe_id, user_id, rating_value):
    """
    Utility function which handles user completing a recipe and rating it. Once user has used recipe, the function
    will delete the recipe from the "recipe in-use list" for the user. The rating provided by user is saved and updates
    the overall recipe rating.
    """
    # Query to find the in-use recipe for the user
    in_use_recipe = InUseRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if not in_use_recipe:
        return {'error': 'In-use recipe not found'}

    # Delete the in-use recipe
    db.session.delete(in_use_recipe)

    # If a rating value is provided, save it
    if rating_value:
        save_rating(user_id, recipe_id, int(rating_value))

    db.session.commit()
    return {'success': 'Recipe completed and rated successfully!'}


def create_shopping_list_from_recipe(recipe_id, user_id):
    user: User = User.query.filter_by(id=user_id).first()
    recipe: Recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return {'error': 'Recipe not found'}

    user_pantry = user.get_pantry()
    pantry_dict = {item.get_name(): item for item in user_pantry}

    shopping_list = ShoppingList.query.filter_by(user_id=user_id, list_name=recipe.name).first()
    if not shopping_list:
        shopping_list = create_shopping_list_util(user_id=user_id, list_name=f"Ingredients needed for {recipe.get_name()}")

    for ingredient in recipe.ingredients:
        qfi_ingredient = ingredient.qfooditem
        if qfi_ingredient:
            ingredient_name = ingredient.get_name()
            ingredient_quantity = ingredient.get_quantity()
            pantry_item = pantry_dict.get(ingredient_name)

            if pantry_item:     # Item is already in pantry. Need to check if quantity is sufficient
                amount = ingredient_quantity - pantry_item.get_quantity()
                if amount:          # If amount is positive (not enough of the ingredient in pantry)
                    create_shopping_item(list_id=shopping_list.id, food=ingredient_name, quantity=amount,
                                         units=ingredient.get_units())
            else:               # Item is not present in pantry hence add item with required quantity
                create_shopping_item(list_id=shopping_list.id, food=ingredient_name, quantity=ingredient_quantity,
                                     units=ingredient.get_units())

                db.session.commit()

    return {'success': 'Shopping list created'}
