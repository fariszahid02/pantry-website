# Authored by: Keirav, Yat Nam, Joe, Jawaher, Faris
# View functions for recipe pages
from extensions import db
from models import Recipe, Ingredient, QuantifiedFoodItem, Rating, PantryItem, InUseRecipe, FoodItem, ShoppingItem, ShoppingList
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from recipes.forms import RecipeForm
from recipes.recipe_util import (create_recipe, create_or_get_food_item, create_and_get_qfid,
                                 delete_recipe_instance, update_recipe_rating, create_shopping_list_from_recipe,
                                 save_rating, complete_and_rate_recipe, get_pantry_dict, check_recipe_ingredients)

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

print("Template folder:", recipes_blueprint.template_folder)

# Filter system to sort recipes based on name, calories, rating, etc.
@recipes_blueprint.route('/recipes', methods=['GET'])
@login_required
def recipes():
    can_make_recipe_filter = request.args.get('can_make', type=bool)
    sort_by = request.args.get('sort_by', 'name')
    min_calories = request.args.get('min_calories', type=int)
    max_calories = request.args.get('max_calories', type=int)
    min_rating = request.args.get('min_rating', type=int)
    ingredient_filter = request.args.get('ingredient')
    serves_filter = request.args.get('serves', type=int)

    user_pantry = current_user.get_pantry()
    pantry_dict = {}
    for item in user_pantry:
        qfi = item.qfooditem
        if qfi.fooditem.name not in pantry_dict:
            pantry_dict[qfi.fooditem.name] = 0
        pantry_dict[qfi.fooditem.name] += qfi.quantity

    query = Recipe.query

    # Filter calories
    if min_calories is not None:
        query = query.filter(Recipe.calories >= min_calories)
    if max_calories is not None:
        query = query.filter(Recipe.calories <= max_calories)

    # Filter rating
    if min_rating is not None:
        query = query.filter(Recipe.rating >= min_rating)

    # Filter ingredients
    if ingredient_filter:
        query = query.join(Recipe.ingredients).join(Ingredient.qfooditem).join(FoodItem).filter(
            FoodItem.name.ilike(f"%{ingredient_filter}%"))

    # Filter servings
    if serves_filter:
        query = query.filter(Recipe.serves == serves_filter)

    # Sorting
    if sort_by == 'calories':
        query = query.order_by(Recipe.calories)
    elif sort_by == 'rating':
        query = query.order_by(Recipe.rating.desc())
    else:
        query = query.order_by(Recipe.name)

    # Execute the search
    recipes = query.all()

    # Consider which user can make the recipe
    if can_make_recipe_filter:
        filtered_recipes = []
        for recipe in recipes:
            can_make_recipe = True
            for ingredient in recipe.ingredients:
                ingredient_name = ingredient.get_name()
                if ingredient_name not in pantry_dict:
                    can_make_recipe = False
                    print(f"Missing ingredient: {ingredient_name}")
                    break
                if pantry_dict[ingredient_name] < ingredient.get_quantity():
                    can_make_recipe = False
                    print(f"Not enough quantity for ingredient: {ingredient_name}")
                    break
            if can_make_recipe:
                filtered_recipes.append(recipe)
        recipes = filtered_recipes

    return render_template('recipes/recipes.html', recipes=recipes)


# View own recipes
@recipes_blueprint.route('/your_recipes')
@login_required
def your_recipes():
    user_id = current_user.id
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return render_template('recipes/your_recipes.html', recipes=recipes)


@recipes_blueprint.route('/recipes_detail/<int:recipe_id>')
@login_required
def recipes_detail(recipe_id):
    """
    This function provides the details of a recipe, checks if the user can make it with their pantry items, and
    identifies any missing ingredients
    """
    # Retrieve the recipe by ID
    recipe = Recipe.query.get(recipe_id)

    # Retrieve all ingredients for the recipe
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()

    # Retrieve the user's pantry items
    user_pantry = PantryItem.query.filter_by(user_id=current_user.id).all()

    # Convert pantry items to a dictionary format for easy read
    pantry_dict = get_pantry_dict(user_pantry)

    # Check if the user can make the recipe with their pantry items and identify any missing ingredients
    can_make_recipe, missing_ingredients = check_recipe_ingredients(ingredients, pantry_dict)

    return render_template('recipes/recipes_detail.html', recipe=recipe, ingredients=ingredients,
                           can_make_recipe=can_make_recipe, missing_ingredients=missing_ingredients)


# Add recipe
@recipes_blueprint.route('/add_recipes', methods=['GET', 'POST'])
@login_required
def add_recipes():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        method = request.form['method']
        serves = request.form['serves']
        calories = request.form['calories']
        ingredients = []

        for i in range(len(request.form.getlist('ingredient[]'))):
            ingredients.append({
                "food": request.form.getlist('ingredient[]')[i],
                "quantity": request.form.getlist('quantity[]')[i],
                "unit": request.form.getlist('unit[]')[i],
            })

        create_recipe(name, method, serves, calories, ingredients)
        return redirect(url_for('recipes.recipes'))  # Ensure this redirects to the correct view
    else:
        return render_template('recipes/add_recipes.html')


# Edit own recipe
@recipes_blueprint.route('/edit_recipes/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipes(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.method = request.form['method']
        recipe.serves = request.form['serves']
        recipe.calories = request.form['calories']

        # Clear existing ingredients
        Ingredient.query.filter_by(recipe_id=recipe_id).delete()

        # Add new ingredients
        ingredients = zip(request.form.getlist('ingredient[]'), request.form.getlist('quantity[]'), request.form.getlist('unit[]'))
        for food, quantity, unit in ingredients:
            food_item = create_or_get_food_item(food)
            qfi = create_and_get_qfid(food_item.id, quantity, unit)
            new_ingredient = Ingredient(recipe_id=recipe_id, qfood_id=qfi)
            db.session.add(new_ingredient)

        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipes.recipes'))
    else:
        ingredients = [(i.qfooditem.fooditem.name, i.qfooditem.quantity, i.qfooditem.units) for i in recipe.ingredients]
        return render_template('recipes/edit_recipes.html', recipe=recipe, ingredients=ingredients)


# Delete own recipe
@recipes_blueprint.route('/delete_recipe/<int:recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe_to_delete = Recipe.query.filter_by(id=recipe_id).first()
    delete_recipe_instance(recipe_to_delete)
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('recipes.recipes'))


@recipes_blueprint.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    rating_value = request.form.get('rating')
    if not rating_value:
        flash('Please select a rating.', 'error')
        return redirect(url_for('recipes.recipes', recipe_id=recipe_id))

    # Use the utility function to save the rating
    save_rating(current_user.id, recipe_id, int(rating_value))
    flash('Thank you for rating!', 'success')

    # Update recipe rating using the utility function
    update_recipe_rating(recipe_id)

    return redirect(url_for('recipes.recipes', recipe_id=recipe_id))


@recipes_blueprint.route('/use_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def use_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        print(f"Recipe with ID {recipe_id} not found")
        return jsonify({'error': 'Recipe not found'}), 404

    user_pantry = PantryItem.query.filter_by(user_id=current_user.id).all()
    pantry_dict = {item.qfooditem.fooditem.name: item for item in user_pantry}

    # Debugging: Print the user's pantry
    print("User Pantry:")
    for item in user_pantry:
        qfi = QuantifiedFoodItem.query.get(item.qfood_id)
        print(f"Pantry Item: {qfi.fooditem.name}, Quantity: {qfi.quantity}, ID: {item.qfood_id}")

    # Debugging: Check if the user has enough ingredients
    print("Recipe Ingredients:")
    for ingredient in recipe.ingredients:
        qfi_ingredient = QuantifiedFoodItem.query.get(ingredient.qfood_id)
        if qfi_ingredient:
            ingredient_name = qfi_ingredient.fooditem.name
            ingredient_quantity = qfi_ingredient.quantity
            print(f"Ingredient: {ingredient_name}, Quantity: {ingredient_quantity}, ID: {ingredient.qfood_id}")

            pantry_item = pantry_dict.get(ingredient_name)
            if not pantry_item:
                print(f"Missing ingredient: {ingredient_name}")
                return jsonify({'error': f'Not enough {ingredient_name} in pantry'}), 400
            if pantry_item.qfooditem.quantity < ingredient_quantity:
                print(f"Not enough quantity for ingredient: {ingredient_name}")
                return jsonify({'error': f'Not enough {ingredient_name} in pantry'}), 400
        else:
            print(f"QuantifiedFoodItem with ID {ingredient.qfood_id} not found")
            return jsonify({'error': 'Internal error: Ingredient data missing'}), 500

    # Add recipe to InUseRecipe
    in_use_recipe = InUseRecipe(user_id=current_user.id, recipe_id=recipe_id)
    db.session.add(in_use_recipe)
    print("Added recipe to InUseRecipe")

    # Delete corresponding ingredients from user's pantry
    for ingredient in recipe.ingredients:
        qfi_ingredient = QuantifiedFoodItem.query.get(ingredient.qfood_id)
        if qfi_ingredient:
            ingredient_name = qfi_ingredient.fooditem.name
            ingredient_quantity = qfi_ingredient.quantity

            pantry_item = pantry_dict.get(ingredient_name)
            if pantry_item.qfooditem.quantity > ingredient_quantity:
                pantry_item.qfooditem.quantity -= ingredient_quantity
                print(f"Updated pantry item: {ingredient_name}, New Quantity: {pantry_item.qfooditem.quantity}")
            else:
                db.session.delete(pantry_item)
                print(f"Deleted pantry item: {ingredient_name}")

    db.session.commit()
    print("Committed changes to the database")
    return jsonify({'success': 'Recipe is now in use'})

# Viewing in-use recipes
@recipes_blueprint.route('/in_use_recipes')
@login_required
def in_use_recipes():
    in_use_recipes = InUseRecipe.query.filter_by(user_id=current_user.id).all()
    recipes = [in_use.recipe for in_use in in_use_recipes]
    return render_template('recipes/in_use_recipes.html', recipes=recipes)


@recipes_blueprint.route('/recipes/complete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def complete_recipe(recipe_id):
    """
    This function routes user to complete a recipe after used and provide a rating. Calls the complete_and_rate_recipe
    utility function from recipe_util.py to handle this logic.
    """
    # Call the utility function to complete and rate the recipe
    response = complete_and_rate_recipe(recipe_id, current_user.id, request.form.get('rating'))

    # Check for errors in the response
    if 'error' in response:
        flash(response['error'], 'danger')
        return redirect(url_for('recipes.in_use_recipes'))

    # Flash success message if no errors
    flash('Recipe completed and rated successfully!', 'success')
    return redirect(url_for('recipes.in_use_recipes'))


# Create shopping list from a recipe
@recipes_blueprint.route('/create_shopping_list/<int:recipe_id>', methods=['POST'])
@login_required
def create_shopping_list(recipe_id):
    response = create_shopping_list_from_recipe(recipe_id, current_user.id)
    if 'error' in response:
        return jsonify(response), 400
    flash("Shopping list created based on recipe", "success")
    return jsonify(response)
