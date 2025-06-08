# Authored by: Yat Nam
# This file handles functionality related to admin users
from models import Recipe, ShoppingList, Rating, PantryItem, WastedFood, Ingredient, ShoppingItem, Barcode, \
    QuantifiedFoodItem, User
from app import db


def delete_user_related_data(user_id):
    """
       Delete all data related to a specific user from the database.

       This function will delete the user's recipes, ratings, shopping lists, pantry items, wasted food entries,
       ingredients, shopping items, barcodes, quantified food items, and finally the user itself.
    """

    # Query all recipes, ratings, shopping lists, pantry items, and wasted food entries for the user
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    ratings = Rating.query.filter_by(user_id=user_id).all()
    shopping_lists = ShoppingList.query.filter_by(user_id=user_id).all()
    pantry_items = PantryItem.query.filter_by(user_id=user_id).all()
    wasted_foods = WastedFood.query.filter_by(user_id=user_id).all()

    # Set to track quantified food items to be deleted
    qfood_items_to_delete = set()

    # Delete all ingredients associated with the user's recipes and the recipes themselves
    for recipe in recipes:
        ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()
        for ingredient in ingredients:
            qfood_items_to_delete.add(ingredient.qfood_id)
            db.session.delete(ingredient)
        db.session.delete(recipe)

    # Delete all ratings associated with the user
    for rating in ratings:
        db.session.delete(rating)

    # Delete all items in the user's shopping lists and the shopping lists themselves
    for shopping_list in shopping_lists:
        shopping_items = ShoppingItem.query.filter_by(list_id=shopping_list.id).all()
        for shopping_item in shopping_items:
            qfood_items_to_delete.add(shopping_item.qfood_id)
            db.session.delete(shopping_item)
        db.session.delete(shopping_list)

    # Delete all pantry items associated with the user
    for pantry_item in pantry_items:
        qfood_items_to_delete.add(pantry_item.qfood_id)
        db.session.delete(pantry_item)

    # Delete all wasted food entries associated with the user
    for wasted_food in wasted_foods:
        qfood_items_to_delete.add(wasted_food.qfood_id)
        db.session.delete(wasted_food)

    # Delete all quantified food items and their associated barcodes
    for qfood_id in qfood_items_to_delete:
        barcodes = Barcode.query.filter_by(qfood_id=qfood_id).all()
        for barcode in barcodes:
            db.session.delete(barcode)
        qfood_item = QuantifiedFoodItem.query.get(qfood_id)
        if qfood_item:
            db.session.delete(qfood_item)

    # Finally, deletes the user
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)

    db.session.commit()