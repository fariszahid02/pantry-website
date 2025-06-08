# Authored by: Yat Nam, Jacob, Keirav
# Test file for shopping_util.py

import unittest
import models
from app import create_app
from populate_db import add_sample_users, add_food_items
import shopping.shopping_util as su


class TestShoppingUtils(unittest.TestCase):

    def setUp(self) -> None:
        models.init_db()
        add_sample_users()
        add_food_items()

    def test_create_shopping_list_util(self) -> None:
        new_list = su.create_shopping_list_util(user_id=3, list_name="Test List")
        expected = models.ShoppingList.query.filter_by(user_id=3, list_name="Test List").first()
        self.assertEqual(new_list, expected, msg="Create Shopping List Failed")

    def test_create_shopping_item(self) -> None:
        new_list = su.create_shopping_list_util(user_id=3, list_name="Test List 2")
        shopping_item = su.create_shopping_item(list_id=new_list.id, food="Butter", quantity=10, units='g')
        expected = models.ShoppingItem.query.filter_by(id=shopping_item.id).first()
        equiv = shopping_item.id == expected.id and shopping_item.get_name() == expected.get_name() and \
            shopping_item.get_quantity() == expected.get_quantity()

        self.assertTrue(equiv, msg="Create Shopping Item Failed")

    def test_delete_shopping_item(self) -> None:
        new_list = su.create_shopping_list_util(user_id=3, list_name="Test List 3")
        shopping_item = su.create_shopping_item(list_id=new_list.id, food="Butter", quantity=10, units='g')
        associated_qfood_id = shopping_item.qfooditem.id

        su.delete_shopping_item(shopping_item.id)
        shopping_item = models.ShoppingItem.query.filter_by(id=shopping_item.id).first()
        qfooditem = models.QuantifiedFoodItem.query.filter_by(id=associated_qfood_id).first()
        result = shopping_item or qfooditem         # Should evaluate to False
        self.assertFalse(result, msg="Delete Shopping Item Failed")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        unittest.main(exit=False)
