# View functions for the shopping HTML template
# Authored by Jacob Norman and Yat Nam Chan

from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import current_user, login_required

from models import ShoppingList, ShoppingItem
from shopping.forms import AddItemForm, CreateListForm
from shopping.shopping_util import create_shopping_list_util, create_shopping_item, \
    delete_shopping_item, delete_shopping_list, mark_shopping_list_as_complete

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')


# Base view function that initially renders shopping list page
@shopping_blueprint.route('/shopping_list', methods=['GET'])
@login_required
def shopping_list():
    user_shopping_lists = ShoppingList.query.filter_by(user_id=current_user.id).all()
    return render_template('shopping/shopping_list.html', shopping_lists=user_shopping_lists)


# takes user input of a new list name, creates that list then redirects user to a page to add first items to the list
@shopping_blueprint.route('/create_shopping_list', methods=['GET', 'POST'])
@login_required
def create_shopping_list():
    form = CreateListForm()
    if request.method == 'POST' and form.validate_on_submit():
        list_name = form.listName.data
        s_list = create_shopping_list_util(current_user.id, list_name)
        flash("Shopping list created", "success")
        return redirect(url_for('shopping.shopping_list_detail', list_id=s_list.id))
    return render_template('shopping/create_shopping_list.html', form=form)


# View function that renders an already existing shopping lists they have and allows user to modify them
@shopping_blueprint.route('/shopping_list_detail/<int:list_id>', methods=['GET', 'POST'])
@login_required
def shopping_list_detail(list_id):
    s_list = ShoppingList.query.get_or_404(list_id)
    form = AddItemForm()
    if request.method == 'POST' and form.validate_on_submit():
        food_item_name = form.newItem.data
        quantity = form.itemQuantity.data
        units = form.itemUnits.data

        create_shopping_item(list_id, food_item_name, quantity, units)

        flash("Item added to shopping list", "success")
        return redirect(url_for('shopping.shopping_list_detail', list_id=list_id))

    return render_template('shopping/shopping_list_detail.html', form=form, shopping_list=s_list)


# View function to delete a shopping list in its entirety
@shopping_blueprint.route('/delete_list/<int:list_id>', methods=['POST'])
@login_required
def delete_list(list_id):
    s_list = ShoppingList.query.get_or_404(list_id)
    if s_list.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list'))

    delete_shopping_list(s_list)
    flash('Shopping list deleted', 'success')
    return redirect(url_for('shopping.shopping_list'))


# View function for deleting a food item from a shopping list
@shopping_blueprint.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    shopping_item = ShoppingItem.query.get_or_404(item_id)
    s_list = shopping_item.get_slist()
    if s_list.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list_detail', list_id=shopping_item.list_id))

    delete_shopping_item(item_id)
    flash('Item deleted from shopping list', 'success')
    return redirect(url_for('shopping.shopping_list_detail', list_id=shopping_item.list_id))


# View function to move a single item from shopping list to pantry
@shopping_blueprint.route('/list_to_pantry/<int:item_id>', methods=['POST'])
@login_required
def list_to_pantry(item_id):
    shopping_item = ShoppingItem.query.get_or_404(item_id)
    return redirect((url_for('shopping.shopping_list_detail', list_id=shopping_item.list_id)))

# Example usage in the route
@shopping_blueprint.route('/complete_list/<int:list_id>', methods=['POST'])
@login_required
def complete_list(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    if shopping_list.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list'))

    mark_shopping_list_as_complete(shopping_list)

    flash('Shopping list completed and items moved to pantry', 'success')
    return redirect(url_for('shopping.shopping_list'))


