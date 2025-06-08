# Authored by: Faris, Jawaher, Jacob, Ken, Keirav
# Utility functions for pantry/views.py. Contains methods to query database.

from models import PantryItem, create_and_get_qfid, create_or_get_food_item
from extensions import db


# Method to add a new item to a users pantry by creating a new pantryitem linked to the user.
def create_pantry_item(user_id: int, food_name: str, quantity: str, calories: str, expiry: str) -> PantryItem:
    food_item = create_or_get_food_item(food_name)
    qfood_id = create_and_get_qfid(food_id=food_item.id, quantity=float(quantity), units='g')
    pantry_item = PantryItem(user_id=user_id, qfood_id=qfood_id, expiry=expiry, calories=float(calories))
    db.session.add(pantry_item)
    db.session.commit()
    return pantry_item


# Method to delete a pantry item. The function deletes the qfooditem associated with the pantryitem
# and through the cascading relationship, the pantryitem instance is also deleted.
def delete_pantry_item(item_id: int) -> None:
    item = PantryItem.query.filter_by(id=item_id).first()
    if item:
        db.session.delete(item.qfooditem)
        db.session.commit()
    return
