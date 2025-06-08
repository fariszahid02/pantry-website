# Authored by: Joe Hare & Keirav Shah

# File to add sample data to database instance for testing.

import random
from typing import Dict
from app import create_app
from extensions import db

import models


pantryitems = [
    {"name": "Milk", "expiry_date": "2024-05-10", 'number': '2', 'quantity': 200, 'units': 'ml', 'calories': 200, 'description': 'Dairy milk'},
    {"name": "jelly", "expiry_date": "2024-05-11", 'number': '5', 'quantity': 200, 'units': 'g', 'calories': 250, 'description': 'Fruit jelly'},
    {"name": "pork", "expiry_date": "2024-05-12", 'number': '4', 'quantity': 200,  'units': 'g', 'calories': 350, 'description': 'Pork meat'},
    {"name": "chocolate", "expiry_date": "2024-05-12", 'number': '4', 'quantity': 200, 'units': 'g', 'calories': 360, 'description': 'Dark chocolate'},
    {"name": "Goat Milk", "expiry_date": "2024-05-13", 'number': '2', 'quantity': 200, 'units': 'g', 'calories': 200, 'description': 'Goat milk'},
    {"name": "Bread", "expiry_date": "2024-05-12", 'number': '2', 'quantity': 200, 'units': 'g', 'calories': 100, 'description': 'Whole grain bread'},
    {"name": "Apple", "expiry_date": "2024-04-28", 'number': '5', 'quantity': 200, 'units': 'g', 'calories': 60, 'description': 'Fresh apple'},
    {"name": "Beef", "expiry_date": "2024-06-30", 'number': '5', 'quantity': 200, 'units': 'g', 'calories': 500, 'description': 'Beef meat'},
    {"name": "Lamb", "expiry_date": "2024-09-28", 'number': '3', 'quantity': 200, 'units': 'g', 'calories': 450, 'description': 'Lamb meat'},
    {"name": "Apple juice", "expiry_date": "2024-05-04", 'number': '100', 'quantity': 200, 'units': 'ml', 'calories': 150, 'description': 'Fresh apple juice'},
]

users = [
    {"first_name": "Gillan", "last_name": "Athelstan", "email": "gathelstan0@npr.org", "password": "pO6>#*9hV",
     "dob": "6/2/2023"},
    {"first_name": "Doralyn", "last_name": "Kosel", "email": "dkosel1@noaa.gov", "password": "aX7|S&9hZrRT",
     "dob": "11/27/2023"},
    {"first_name": "Patrice", "last_name": "Ferier", "email": "pferier2@google.it", "password": "bX3%UvGx$nl@g",
     "dob": "7/18/2023"},
    {"first_name": "Dyann", "last_name": "Shaul", "email": "dshaul3@mashable.com", "password": "cO5{hmv_UiO>LDa.",
     "dob": "11/30/2023"},
    {"first_name": "Graeme", "last_name": "Aliman", "email": "galiman4@discuz.net", "password": "vX5$0rJyY20=|",
     "dob": "6/14/2023"},
    {"first_name": "Rutledge", "last_name": "Dicey", "email": "rdicey5@ning.com", "password": "vG6\\XecCNVG`#di(",
     "dob": "3/11/2024"},
    {"first_name": "Arleyne", "last_name": "Ianetti", "email": "aianetti6@xinhuanet.com", "password": "kQ0.B4!@wuUp#7u",
     "dob": "4/9/2024"},
    {"first_name": "Jemmy", "last_name": "Sambals", "email": "jsambals7@narod.ru", "password": "lY2*_{*\\F'CZ7Y",
     "dob": "8/6/2023"},
    {"first_name": "Leila", "last_name": "Jirek", "email": "ljirek8@addthis.com", "password": "yR6~).,!2+`R",
     "dob": "11/29/2023"},
    {"first_name": "Chrysler", "last_name": "Quemby", "email": "cquemby9@dion.ne.jp", "password": "eB3_Xk\\f",
     "dob": "4/2/2024"}
]
userObjects = []

foodItems = [
    {"name": "Apple", "description": "Fresh apple"},
    {"name": "Tofu", "description": "Soft tofu"},
    {"name": "Spaghetti", "description": "Dry spaghetti pasta"},
    {"name": "Eggs", "description": "Chicken eggs"},
    {"name": "Butter", "description": "Salted butter"},
    {"name": "Water", "description": "Bottled water"},
    {"name": "Cornstarch", "description": "Corn starch powder"},
    {"name": "Flour", "description": "All-purpose flour"},
    {"name": "Jasmine Rice", "description": "Fragrant jasmine rice"},
    {"name": "Basmati Rice", "description": "Long-grain basmati rice"},
    {"name": "Vegetable Oil", "description": "Cooking vegetable oil"},
    {"name": "Olive Oil", "description": "Extra virgin olive oil"},
    {"name": "Cocoa Powder", "description": "Unsweetened cocoa powder"},
    {"name": "Oats", "description": "Rolled oats"},
    {"name": "Chicken Thigh", "description": "Chicken thigh meat"},
    {"name": "Chicken breast", "description": "Chicken breast meat"},
    {"name": "Minced Beef", "description": "Ground beef"},
    {"name": "Minced Pork", "description": "Ground pork"},
    {"name": "Duck breast", "description": "Duck breast meat"},
    {"name": "Cinnamon", "description": "Ground cinnamon"},
    {"name": "Garlic", "description": "Fresh garlic"},
    {"name": "Onion", "description": "Yellow onion"},
    {"name": "Shallot", "description": "Fresh shallot"},
    {"name": "Spring Onion", "description": "Green onions"},
    {"name": "Galangal", "description": "Fresh galangal"},
    {"name": "Ginger", "description": "Fresh ginger root"},
    {"name": "Rendang", "description": "Rendang curry paste"},
    {"name": "Anchovies", "description": "Salted anchovies"},
    {"name": "Peanuts", "description": "Roasted peanuts"},
    {"name": "Coconut", "description": "Grated coconut"},
    {"name": "Salmon Fillet", "description": "Salmon fish fillet"},
    {"name": "White Miso", "description": "White miso paste"},
    {"name": "Red Miso", "description": "Red miso paste"},
    {"name": "Parsnip", "description": "Fresh parsnip"},
    {"name": "Pork Loin", "description": "Pork loin meat"},
    {"name": "Peanut Oil", "description": "Cooking peanut oil"},
    {"name": "Carrot", "description": "Fresh carrot"},
    {"name": "Dashi", "description": "Dashi stock"},
    {"name": "Beef Chuck", "description": "Beef chuck roast"},
    {"name": "Pesto", "description": "Basil pesto sauce"},
    {"name": 'Tomatoes', "description": "Fresh tomatoes"},
    {"name": 'Fresh Mozzarella', "description": "Fresh mozzarella cheese"},
    {"name": 'Fresh Basil Leaves', "description": "Fresh basil leaves"},
    {"name": 'Extra Virgin Olive Oil', "description": "High-quality olive oil"},
    {"name": 'Balsamic Vinegar', "description": "Aged balsamic vinegar"},
    {"name": 'Salt', "description": "Table salt"},
    {"name": 'Pepper', "description": "Black pepper"},
    {"name": 'Banana', "description": "Fresh banana"},
    {"name": 'Peanut Butter', "description": "Creamy peanut butter"},
    {"name": 'Milk', "description": "Dairy milk"},
    {"name": 'Eggs', "description": "Chicken eggs"},
    {"name": 'Butter', "description": "Salted butter"},
    {"name": 'Avocado', "description": "Fresh avocado"},
    {"name": 'Lime', "description": "Fresh lime"}
]
foodItemObjects = []

recipes = [
    {
        'name': 'Caprese Salad',
        'ingredients': [
            {'ingredient': 'Tomatoes', 'quantity': 3, 'units': ''},
            {'ingredient': 'Fresh Mozzarella', 'quantity': 100, 'units': 'g'},
            {'ingredient': 'Fresh Basil Leaves', 'quantity': 10, 'units': 'g'},
            {'ingredient': 'Extra Virgin Olive Oil', 'quantity': 1, 'units': 'tbsp'},
            {'ingredient': 'Balsamic Vinegar', 'quantity': 1, 'units': 'tbsp'},
            {'ingredient': 'Salt', 'quantity': 2, 'units': 'tspn'},
            {'ingredient': 'Pepper', 'quantity': 2, 'units': 'tspn'}
        ],
        'method': 'Slice tomatoes and fresh mozzarella. Arrange them on a plate, '
                  'alternating slices. Tuck fresh basil leaves in between. Drizzle '
                  'with extra virgin olive oil and balsamic vinegar. Season with salt '
                  'and pepper to taste.'
    },
    {
        'name': 'Peanut Butter Banana Smoothie',
        'ingredients': [
            {'ingredient': 'Banana', 'quantity': 2, 'units': ''},
            {'ingredient': 'Peanut Butter', 'quantity': 1, 'units': 'tbsp'},
            {'ingredient': 'Milk', 'quantity': 100, 'units': 'ml'}
        ],
        'method': 'Peel and slice banana. Put banana slices, peanut butter, and '
                  'milk into a blender. Add honey if desired. Blend until smooth.'
    },
    {
        'name': 'Scrambled Eggs',
        'ingredients': [
            {'ingredient': 'Eggs', 'quantity': 2, 'units': ''},
            {'ingredient': 'Butter', 'quantity': 20, 'units': 'g'},
            {'ingredient': 'Salt', 'quantity': 1, 'units': 'tspn'},
            {'ingredient': 'Pepper', 'quantity': 2, 'units': 'tspn'}
        ],
        'method': 'Crack eggs into a bowl and beat them until yolks and whites are combined. '
                  'Melt butter in a non-stick skillet over medium heat. Pour in beaten eggs. '
                  'Stir occasionally until eggs are set. Season with salt and pepper.'
    },
    {
        'name': 'Guacamole',
        'ingredients': [
            {'ingredient': 'Avocado', 'quantity': 3, 'units': ''},
            {'ingredient': 'Lime', 'quantity': 1, 'units': ''},
            {'ingredient': 'Salt', 'quantity': 2, 'units': 'tspn'}
        ],
        'method': 'Cut avocado in half, remove pit, and scoop out flesh into a bowl. '
                  'Mash avocado with a fork. Squeeze lime juice over mashed avocado '
                  'and mix well. Add salt to taste.'
    }
]
recipeObjects = []

barcodes = [
    {'code': '0512345000107', 'food': 'Olive Oil', 'quantity': '300', 'units': 'ml'},
    {'code': '9300633929169', 'food': 'Minced Pork', 'quantity': '500', 'units': 'g'},
    {'code': '23987234987', 'food': 'Banana', 'quantity': '5', 'units': '#'},
    {'code': '5022032139942', 'food': 'Jasmine Rice', 'quantity': '2', 'units': 'kg'},
    {'code': '6971958734962', 'food': 'White Miso', 'quantity': '100', 'units': 'g'},
]


def add_sample_users():
    for user in users:
        new_user = models.User(email=user['email'],
                               password=user['password'],
                               first_name=user['first_name'],
                               last_name=user['last_name'],
                               dob=user['dob'])
        db.session.add(new_user)
        db.session.flush()
        db.session.refresh(new_user)
        userObjects.append(new_user)
    db.session.commit()


def add_food_items():
    for food in foodItems:
        new_food = models.FoodItem(food_name=food['name'])
        db.session.add(new_food)
        db.session.flush()
        db.session.refresh(new_food)
        foodItemObjects.append(new_food)
    db.session.commit()


def create_quantified_food_item(food_item_id: int, quantity=0) -> models.QuantifiedFoodItem:
    units = ('ml', 'g')
    quantities = (200, 500, 1000, 750, 50, 20)
    quant = quantity if quantity else random.choice(quantities)
    q_fooditem = models.QuantifiedFoodItem(food_id=food_item_id,
                                           quantity=quant,
                                           units=random.choice(units))
    db.session.add(q_fooditem)
    db.session.commit()
    return q_fooditem


def create_and_get_qfid(food_id, quantity, units):
    qfi = models.QuantifiedFoodItem(food_id=food_id,
                                    quantity=quantity,
                                    units=units)
    db.session.add(qfi)
    db.session.commit()
    return qfi.id


def create_pantry_item(user_id: int, rand: bool, qfood_id: int = -1) -> models.PantryItem:
    expiries = ('2024-05-08', '2024-10-11', '2024-08-18', '2024-04-02', '2025-01-01', '2025-03-28', '2024-09-19')
    qfood_item = create_quantified_food_item(random.choice(foodItemObjects).id)
    calories = random.randint(50, 500)
    if rand:
        pantry_item = models.PantryItem(user_id=user_id, qfood_id=qfood_item.id, expiry=random.choice(expiries),
                                        calories=calories)
        db.session.add(pantry_item)
    else:
        pantry_item = models.PantryItem(user_id=user_id, qfood_id=qfood_id, expiry=random.choice(expiries),
                                        calories=calories)
        db.session.add(pantry_item)
    db.session.commit()
    return pantry_item


def create_pantries() -> None:
    for user in userObjects:
        num_items = random.choice((3, 6, 4, 2))
        for i in range(num_items):
            create_pantry_item(user_id=user.id, rand=True)


def create_ingredient(recipe_id: int, qfood_id: int) -> models.Ingredient:
    ingredient = models.Ingredient(recipe_id=recipe_id, qfood_id=qfood_id)
    db.session.add(ingredient)
    db.session.commit()
    return ingredient


def create_recipe_object(user_id: int, recipe, add_ingts_to_pantry: Dict[str, int] = None) -> models.Recipe:
    new_recipe = models.Recipe(user_id=user_id,
                               recipe_name=recipe['name'],
                               cooking_method=recipe['method'],
                               serves=random.choice((1, 2, 4)),
                               calories=random.choice((450, 800, 1200, 1000)))

    db.session.add(new_recipe)
    db.session.flush()                          # flush current objects in session to db
    db.session.refresh(new_recipe)              # refresh new_recipe object to now contain id field
    recipeObjects.append(new_recipe)

    for ingredient in recipe['ingredients']:
        foodItem = models.create_or_get_food_item(ingredient['ingredient'])
        qfoodItem_id = models.create_and_get_qfid(food_id=foodItem.id, quantity=ingredient['quantity'], units=ingredient['units'])
        create_ingredient(recipe_id=new_recipe.id, qfood_id=qfoodItem_id)
        if add_ingts_to_pantry:
            if new_recipe.id == add_ingts_to_pantry['recipe_id']:
                new_qfood_id = models.create_and_get_qfid(food_id=foodItem.id, quantity=ingredient['quantity'], units=ingredient['units'])
                create_pantry_item(user_id=add_ingts_to_pantry['user_id'], rand=False, qfood_id=new_qfood_id)
    db.session.commit()
    return new_recipe


def create_recipes() -> None:
    for recipe in recipes:
        user_id = 1
        create_recipe_object(user_id=user_id, recipe=recipe, add_ingts_to_pantry={'user_id': 2, "recipe_id": 4})


def create_shopping_items(list_id: int) -> models.ShoppingItem:
    qfood_item = create_quantified_food_item(random.choice(foodItemObjects).id)
    shopping_item = models.ShoppingItem(list_id=list_id, qfood_id=qfood_item.id)
    db.session.add(shopping_item)
    db.session.commit()
    return shopping_item


def create_shopping_lists() -> None:
    chosen_users = userObjects[::2]
    example_names = ('Monday Shop', 'Asian Grocery Shop', 'Butchery', 'Bakery', 'Green Grocers', 'Farmers Market')
    for user in chosen_users:
        for x in range(2):
            shopping_list = models.ShoppingList(user_id=user.id, list_name=random.choice(example_names))
            db.session.add(shopping_list)
            db.session.flush()                              # flush current objects in session to db
            db.session.refresh(shopping_list)               # refresh shopping_list object to now contain the id field
            num_items = random.choice((3, 5, 2, 6, 9))
            for i in range(num_items):
                create_shopping_items(list_id=shopping_list.id)


def create_ratings() -> None:
    for recipe in recipeObjects:
        num_ratings = random.choice((2, 3, 5, 7))
        chosen_users = []
        for i in range(num_ratings):
            chosen_user = random.choice(userObjects)
            while chosen_user in chosen_users:
                chosen_user = random.choice(userObjects)
            chosen_users.append(chosen_user)
            rating = random.choice((0, 1, 2, 3, 4, 5))
            new_rating = models.Rating(chosen_user.id, recipe.id, rating)
            db.session.add(new_rating)
    db.session.commit()
    for recipe in recipeObjects:
        recipe.update_rating()


def create_barcodes() -> None:
    for barcode in barcodes:
        food_item = models.create_or_get_food_item(barcode['food'])
        qfood_id = models.create_and_get_qfid(food_id=food_item.id, quantity=float(barcode['quantity']),
                                              units=barcode['units'])
        barcode_item = models.Barcode(qfood_id, barcode['code'])
        db.session.add(barcode_item)
        db.session.commit()


def main():
    # add sample users
    add_sample_users()

    # add sample foodItems
    add_food_items()

    # create pantries
    create_pantries()

    # create recipes
    create_recipes()

    # create ratings
    create_ratings()

    # create shopping lists
    create_shopping_lists()

    # create barcodes
    create_barcodes()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        models.init_db()
        main()
        db.session.commit()
