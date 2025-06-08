# Authored by: Faris, Keirav
# Test file for pantry_util.py

import unittest
import models
from app import create_app
from populate_db import add_sample_users, add_food_items
import pantry.pantry_util as pu


class TestPantryUtils(unittest.TestCase):

    # Setup method to initialize the database and populate it with sample data before each test
    def setUp(self) -> None:
        models.init_db()
        add_sample_users()
        add_food_items()

    # Test case for creating a pantry item
    def test_create_pantry_item(self) -> None:
        # Call the create_pantry_item function with test data
        pantry_item = pu.create_pantry_item(user_id=3, food_name="Apples", quantity="5", calories="250", expiry="2024-12-15")
        expected = models.PantryItem.query.filter_by(user_id=3, qfood_id=pantry_item.qfood_id).first()
        self.assertEqual(pantry_item, expected, msg="Create Pantry Item Failed")

    # Test case for deleting a pantry item
    def test_delete_pantry_item(self) -> None:
        # This creates a pantry item to be deleted
        pantry_item = pu.create_pantry_item(user_id=3, food_name="Bananas", quantity="3", calories="200", expiry="2024-12-15")
        # Call the delete_pantry_item function to delete the created item
        pu.delete_pantry_item(pantry_item.id)
        deleted_item = models.PantryItem.query.filter_by(id=pantry_item.id).first()
        self.assertIsNone(deleted_item, msg="Delete Pantry Item Failed")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        unittest.main(exit=False)
