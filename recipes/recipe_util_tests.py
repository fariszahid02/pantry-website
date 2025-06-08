# Authored by: Faris
# Tests for recipe_util.py
import unittest
import models
from app import create_app
from populate_db import add_sample_users, add_food_items
import recipes.recipe_util as ru


class TestRecipeUtils(unittest.TestCase):

    def setUp(self) -> None:
        models.init_db()
        add_sample_users()
        add_food_items()

    def test_create_recipe(self) -> None:
        # Define ingredients for the recipe
        ingredients = [
            {"food": "Tomatoes", "quantity": 2, "unit": "g"},
            {"food": "Onions", "quantity": 1, "unit": "g"}
        ]
        ru.create_recipe(name="Tomato Soup", method="Boil tomatoes and onions", serving_size=2, calories=100, ingredients=ingredients)
        recipe = models.Recipe.query.filter_by(name="Tomato Soup").first()
        self.assertIsNotNone(recipe, msg="Create Recipe Failed")

    def test_add_ingredient(self) -> None:
        # This creates a recipe with no ingredients
        ru.create_recipe(name="Tomato Soup", method="Boil tomatoes and onions", serving_size=2, calories=100, ingredients=[])
        recipe = models.Recipe.query.filter_by(name="Tomato Soup").first()

        # Call the add_ingredient function to add an ingredient to the recipe
        ru.add_ingredient(ingredient="Garlic", quantity=2, unit="g", recipe_id=recipe.id)
        ingredient = models.Ingredient.query.filter_by(recipe_id=recipe.id).first()
        self.assertIsNotNone(ingredient, msg="Add Ingredient Failed")

    def test_check_recipe_ingredients(self) -> None:
        # Create a sample pantry with items
        user_pantry = [
            models.PantryItem(user_id=1, qfood_id=1, expiry="2024-10-02", calories=50),
            models.PantryItem(user_id=1, qfood_id=2, expiry="2024-10-02", calories=30)
        ]
        # Generate a pantry dictionary from the sample pantry
        pantry_dict = ru.get_pantry_dict(user_pantry)
        # Define ingredients for the recipe
        ingredients = [
            models.Ingredient(recipe_id=1, qfood_id=1),
            models.Ingredient(recipe_id=1, qfood_id=2)
        ]
        # This checks if the ingredients are available in My Pantry
        can_make_recipe, missing_ingredients = ru.check_recipe_ingredients(ingredients, pantry_dict)
        self.assertTrue(can_make_recipe, msg="Check Recipe Ingredients Failed")
        self.assertEqual(missing_ingredients, [], msg="Missing Ingredients Detected")

    def test_update_recipe_rating(self) -> None:
        ru.create_recipe(name="Tomato Soup", method="Boil tomatoes and onions", serving_size=2, calories=100, ingredients=[])
        recipe = models.Recipe.query.filter_by(name="Tomato Soup").first()
        # This calls the create_recipe_rating function to rate the recipe
        ru.create_recipe_rating(user_id=1, recipe_id=recipe.id, rating=5)
        # This calls the update_recipe_rating function to update the recipe's rating
        ru.update_recipe_rating(recipe_id=recipe.id)
        updated_recipe = models.Recipe.query.filter_by(id=recipe.id).first()
        self.assertEqual(updated_recipe.rating, 5, msg="Update Recipe Rating Failed")

    def test_delete_recipe_instance(self) -> None:
        ru.create_recipe(name="Tomato Soup", method="Boil tomatoes and onions", serving_size=2, calories=100, ingredients=[])
        recipe = models.Recipe.query.filter_by(name="Tomato Soup").first()
        # This calls the delete_recipe_instance function to delete the recipe
        ru.delete_recipe_instance(recipe)
        deleted_recipe = models.Recipe.query.filter_by(name="Tomato Soup").first()
        self.assertIsNone(deleted_recipe, msg="Delete Recipe Instance Failed")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        unittest.main(exit=False)
