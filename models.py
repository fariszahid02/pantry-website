# Authored by: Joe, Keirav, Yat Nam
# Create classes to model database
from flask_login import UserMixin
from extensions import db
from datetime import datetime
import bcrypt
from crawler import fetch_wikipedia_description


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # authentication details
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # user details
    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    dob = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

    # security details
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    current_login = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    current_login_ip = db.Column(db.String(45), nullable=True)
    last_login_ip = db.Column(db.String(45), nullable=True)
    total_logins = db.Column(db.Integer, default=0)

    # declaring relationships to other tables
    recipes = db.relationship('Recipe', backref='user')
    ratings = db.relationship('Rating', backref='user')
    shopping_lists = db.relationship('ShoppingList', backref='user')
    pantry = db.relationship("PantryItem", backref="user")
    wasted = db.relationship('WastedFood', backref='user')

    def __init__(self, email, password, first_name, last_name, dob, role='user'):
        self.email = email
        # Hash password before storing in database
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.registered_on = datetime.now()
        self.role = role

    # Method to update last and current logins and ips. Takes current request's ip address.
    def update_security_fields_on_login(self, ip_addr: str) -> None:
        self.last_login = self.current_login
        self.current_login = datetime.now()
        self.last_login_ip = self.current_login_ip
        self.current_login_ip = ip_addr
        self.total_logins += 1
        db.session.commit()

    def verify_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def set_password(self, password) -> None:
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.session.commit()

    # Method to get user's shoppings lists. Returns a list of ShoppingList objects i.e. List[ShoppingList]
    def get_shopping_lists(self):
        return self.shopping_lists

    # Method to get items in user's pantry. Returns a list of PantryItem objects i.e. List[PantryItem]
    def get_pantry(self):
        return self.pantry

    # Method to get all recipes that a user has created. Returns a list of Recipe objects i.e. List[Recipe]
    def get_recipes(self):
        return self.recipes

    # Method to get all recipe ratings a user has given. Returns a list of Rating objects i.e. List[Rating]
    def get_ratings(self):
        return self.ratings

    # Method to get a string representation of all the uesr's shopping lists
    def get_shopping_lists_str(self):
        numlists = len(self.shopping_lists)
        output = f'Number of lists {numlists}\n' + '\n'.join([f'list ({i+1}/{numlists})\n{slist.__str__()}' for i, slist
                                                              in enumerate(self.shopping_lists)])
        return output

    def print_pantry(self) -> None:
        print(f"USER {self.id} PANTRY")
        pantry = "\n".join([item.__str__() for item in self.get_pantry()])
        print(pantry)

    def get_qfoods_pantry(self):  # -> List[QuantifiedFoodItem]
        return [pantryitem.qfooditem for pantryitem in self.get_pantry()]

    def is_admin(self) -> bool:
        return self.role == 'admin'


class Recipe(db.Model):
    __tablename__ = 'recipes'

    # Recipe details
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    method = db.Column(db.Text, nullable=False)
    serves = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)

    # Links to other tables
    ingredients = db.relationship("Ingredient", cascade="all, delete", backref='recipe')
    compatible_diets = db.relationship("CompatibleDiet", backref='recipe')
    ratings = db.relationship("Rating", cascade="all, delete", backref='recipe')

    def __init__(self, user_id, recipe_name, cooking_method, serves, calories):
        self.user_id = user_id
        self.name = recipe_name
        self.method = cooking_method
        self.serves = serves
        self.calories = calories
        self.rating = 0

    def __str__(self):
        ingredient_block = 'Ingredients: \n' + '\n'.join([ingredient.__str__() for ingredient in self.ingredients])
        output = (f'{self.name}\n{ingredient_block}\nServes: {self.serves}\nCalories: {self.calories}\n'
                  f'Rating: {self.rating}\n{self.method}\n')
        return output

    def get_ingredients_str(self):
        ingredient_block = 'Ingredients: \n' + f'\n'.join([f'{i+1}) {ingredient.__str__()}\n' for i, ingredient in
                                                           enumerate(self.ingredients)])
        return ingredient_block

    # Method to get the recipe's name
    def get_name(self) -> str:
        return self.name

    # Method to get the recipe's cooking method
    def get_method(self) -> str:
        return self.method

    # Method to get the number of people the recipe serves
    def get_serves(self) -> int:
        return self.serves

    # Method to get the number of calories the recipe contains
    def get_calories(self) -> int:
        return self.calories

    # Method to get the recipe's rating
    def get_rating(self) -> float:
        self.update_rating()
        return self.rating

    # Method to get recipe's ingredients
    def get_ingredients(self):
        return self.ingredients

    # Method to update recipe's rating attribute. Made for internal use (shouldn't need to be called from front end)
    def update_rating(self):
        ratings = self.ratings
        avg_rating = sum([rating.get_rating() for rating in ratings]) / len(ratings)
        self.rating = round(avg_rating * 2) / 2         # Round to nearest 0.5
        db.session.commit()

    def get_qfoods_ingredients(self):     # -> List[QuantifiedFoodItem]
        return [ingredient.qfooditem for ingredient in self.get_ingredients()]


class Rating(db.Model):
    __tablename__ = 'ratings'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), primary_key=True, nullable=False)
    rating = db.Column(db.Integer)              # Need to validate that incoming value is between 0 & 5

    def __init__(self, user_id: int, recipe_id: int, rating: int):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.rating = rating

    def get_rating(self) -> int:
        return self.rating

    def set_rating(self, rating: int) -> None:
        self.rating = rating
        db.session.commit()


class ShoppingList(db.Model):
    __tablename__ = 'shoppinglists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    list_name = db.Column(db.String(50), nullable=False)

    # Declaring relationship shopping item table
    shopping_items = db.relationship('ShoppingItem', cascade="all, delete", backref="slist")

    def __init__(self, user_id, list_name):
        self.user_id = user_id
        self.list_name = list_name

    def __str__(self):
        items = self.shopping_items
        output = f'{self.list_name}\n' + f'\n'.join([f'{i+1}: {item.qfooditem.__str__()}' for i, item in enumerate(items)])
        return output

    def get_name(self) -> str:
        return self.list_name

    def set_name(self, list_name: str) -> None:
        self.list_name = list_name
        db.session.commit()

    def get_items(self):    # -> List[ShoppingItem]
        return self.shopping_items


class FoodItem(db.Model):
    __tablename__ = 'fooditems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)

    # Declaring relationships to other tables
    quantified_food_item = db.relationship('QuantifiedFoodItem', backref='fooditem')

    def __init__(self, food_name):
        # 转换名称为首字母大写，其余小写，保留单个空格
        formatted_name = ' '.join(word.capitalize() for word in food_name.strip().split())
        self.name = formatted_name
        self.description = fetch_wikipedia_description(formatted_name)

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description


class QuantifiedFoodItem(db.Model):
    __tablename__ = 'quantifiedfooditem'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey(FoodItem.id), nullable=False)
    quantity = db.Column(db.Float, default=0.0)
    units = db.Column(db.String(5), default="g")

    # References to other tables
    shopping = db.relationship('ShoppingItem', backref="qfooditem")
    ingredients = db.relationship('Ingredient', backref="qfooditem")
    pantries = db.relationship('PantryItem', cascade="all, delete", backref="qfooditem")
    wasted = db.relationship('WastedFood', backref="qfooditem")
    barcodes = db.relationship('Barcode', backref="qfooditem")

    def __init__(self, food_id, quantity, units):
        self.food_id = food_id
        self.quantity = quantity
        self.units = units

    def __str__(self):
        return f'{self.fooditem.get_name()}, {self.quantity}{self.units}'

    def __eq__(self, other):
        return self.food_id == other.food_id and self.quantity == other.quantity

    def __lt__(self, other):
        return self.food_id == other.food_id and self.quantity < other.quantity

    def __gt__(self, other):
        return self.food_id == other.food_id and self.quantity > other.quantity

    # Method to return the difference in amounts compared to another qfooditem
    def compare_amounts(self, other) -> float:
        difference = self.quantity - other.quantity
        return difference

    def set_quantity(self, quantity: float) -> None:
        self.quantity = quantity
        db.session.commit()

    def set_units(self, units: str) -> None:
        self.units = units
        db.session.commit()

    def get_name(self) -> str:
        return self.fooditem.get_name()

    def get_quantity(self) -> float:
        return self.quantity

    def get_units(self) -> str:
        return self.units


class ShoppingItem(db.Model):
    __tablename__ = 'shoppingitems'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey(ShoppingList.id, ondelete='CASCADE'), nullable=True)
    qfood_id = db.Column(db.String(50), db.ForeignKey(QuantifiedFoodItem.id), nullable=True)

    def __init__(self, list_id, qfood_id):
        self.list_id = list_id
        self.qfood_id = qfood_id

    def get_slist(self) -> ShoppingList:
        return self.slist

    def get_quantity(self) -> float:
        return self.qfooditem.get_quantity()

    def get_units(self) -> str:
        return self.qfooditem.get_units()

    def set_quantity(self, quantity: float) -> None:
        self.qfooditem.qfood.set_qauntity(quantity)

    def set_units(self, units: str) -> None:
        self.qfooditem.set_units(units)

    def get_name(self) -> str:
        return self.qfooditem.get_name()


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id, ondelete='CASCADE'), nullable=True)
    qfood_id = db.Column(db.Integer, db.ForeignKey(QuantifiedFoodItem.id), nullable=True)

    def __init__(self, recipe_id, qfood_id):
        self.recipe_id = recipe_id
        self.qfood_id = qfood_id

    def __str__(self) -> str:
        return f'{self.qfooditem.__str__()}'

    def __repr__(self) -> str:
        return f'<Ingredient(id: {self.id}<Qfooditem({self.qfooditem.__str__()}>>'

    def __eq__(self, other) -> bool:
        return self.qfooditem == other.qfooditem

    def __lt__(self, other):
        return self.qfooditem.__lt__(other.qfooditem)

    def __gt__(self, other):
        return self.qfooditem > other.qfooditem

    def get_quantity(self) -> float:
        return self.qfooditem.get_quantity()

    def get_units(self) -> str:
        return self.qfooditem.get_units()

    def set_quantity(self, quantity: float) -> None:
        self.qfooditem.qfood.set_qauntity(quantity)

    def set_units(self, units: str) -> None:
        self.qfooditem.set_units(units)

    def get_name(self) -> str:
        return self.qfooditem.get_name()


class PantryItem(db.Model):
    __tablename__ = 'pantryitems'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    qfood_id = db.Column(db.Integer, db.ForeignKey(QuantifiedFoodItem.id, ondelete='CASCADE'), nullable=True)
    expiry = db.Column(db.String(10), nullable=True)
    calories = db.Column(db.Integer, nullable=True)

    def __init__(self, user_id, qfood_id, expiry, calories):
        self.user_id = user_id
        self.qfood_id = qfood_id
        self.expiry = expiry
        self.calories = calories

    def __str__(self) -> str:
        return f'<{self.qfooditem.__str__()}, {self.expiry}>'

    def __eq__(self, other) -> bool:
        return self.qfooditem == other.qfooditem

    def __lt__(self, other):
        return self.qfooditem < other.qfooditem

    def __gt__(self, other):
        return self.qfooditem > other.qfooditem

    def get_expiry(self) -> str:
        return self.expiry

    def set_expiry(self, expiry: str) -> None:
        self.expiry = expiry
        db.session.commit()

    def get_quantity(self) -> float:
        return self.qfooditem.get_quantity()

    def get_units(self) -> str:
        return self.qfooditem.get_units()

    def set_quantity(self, quantity: float) -> None:
        self.qfooditem.set_quantity(quantity)

    def set_units(self, units: str) -> None:
        self.qfooditem.set_units(units)

    def get_name(self) -> str:
        return self.qfooditem.get_name()

    def get_calories(self) -> int:
        return self.calories

    def get_food_id(self) -> int:
        return self.qfooditem.food_id


class WastedFood(db.Model):
    __tablename__ = 'wastedfood'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    qfood_id = db.Column(db.Integer, db.ForeignKey(QuantifiedFoodItem.id), nullable=False)
    expired = db.Column(db.String(10), nullable=True)

    def __init__(self, user_id, qfood_id, expired):
        self.user_id = user_id
        self.qfood_id = qfood_id
        self.expired = expired

    def get_expired(self) -> str:
        return self.expired

    def get_name(self) -> str:
        return self.qfooditem.get_name()

    def get_quantity(self) -> float:
        return self.qfooditem.get_quantity()

    def get_units(self) -> str:
        return self.qfooditem.get_units()

class Barcode(db.Model):
    __tablename__ = 'barcodes'

    id = db.Column(db.Integer, primary_key=True)
    qfood_id = db.Column(db.Integer, db.ForeignKey(QuantifiedFoodItem.id), nullable=False)  # Establish link to food table
    barcode = db.Column(db.String(15), nullable=False)

    def __init__(self, qfood_id, barcode):
        self.qfood_id = qfood_id
        self.barcode = barcode

    def get_name(self) -> str:
        return self.qfooditem.get_name()

    def get_quantity(self) -> float:
        return self.qfooditem.get_quantity()

    def get_units(self) -> str:
        return self.qfooditem.get_units()

class Diet(db.Model):
    __tablename__ = 'diet'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(30), nullable=False, unique=True)

    # link to other tables
    compatibleDiet = db.relationship('CompatibleDiet')

    def __init__(self, description):
        self.description = description

class CompatibleDiet(db.Model):
    __tablename__ = 'compatiblediet'
    id = db.Column(db.Integer, primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey(Diet.id), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), nullable=False)

    def __init__(self, diet_id, recipe_id):
        self.diet_id = diet_id
        self.recipe_id = recipe_id


class InUseRecipe(db.Model):
    __tablename__ = 'in_use_recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), nullable=False)

    user = db.relationship(User, backref=db.backref("in_use_recipes", cascade="all, delete-orphan"))
    recipe = db.relationship(Recipe, backref=db.backref("in_use_recipes", cascade="all, delete-orphan"))

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id


# Method to create a new QuantifiedFoodItem.
# Returns the id of the newly created qfooditem.
def create_and_get_qfid(food_id, quantity, units) -> int:
    qfi = QuantifiedFoodItem(food_id=food_id,
                             quantity=quantity,
                             units=units)
    db.session.add(qfi)
    db.session.commit()
    db.session.refresh(qfi)
    return qfi.id


# Method to either retrieve a food item with matching food_name from db.
# If no food item with the name exists, a new instance is created with the name
# and returned.
def create_or_get_food_item(food_name) -> FoodItem:
    food = FoodItem.query.filter_by(name=food_name).first()
    if food is None:  # Add a new food_item to the database if queried food doesn't already exist
        food = FoodItem(food_name=food_name)
        db.session.add(food)
        db.session.commit()
    return food


from models import User


def init_db():
    from app import create_app
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email='admin@email.com',
                     password='Admin1!',
                     first_name='Alice',
                     last_name='Jones',
                     dob='12/09/2001',
                     role='admin')
        db.session.add(admin)
        db.session.commit()
