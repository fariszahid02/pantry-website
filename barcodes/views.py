# Authored by: Joe
# This file handles the functionality for the barcode form and auto filling barcode values
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from barcodes.forms import BarcodeForm
from barcodes.barcode_util import create_barcode, scan_barcode_webcam, scan_barcode_file

barcodes_blueprint = Blueprint('barcodes', __name__, template_folder='templates')


@barcodes_blueprint.route('/add_barcode', methods=['GET', 'POST'])
@login_required
def add_barcode():
    form = BarcodeForm()
    if request.method == 'POST' and form.validate_on_submit():
        barcode = form.barcode.data
        food_item_name = form.food.data
        quantity = form.quantity.data
        units = form.units.data
        create_barcode(barcode, food_item_name, quantity, units)

    return render_template('barcodes/add_barcode.html', form=form)


@barcodes_blueprint.route('/get-barcode-value', methods=['GET'])
@login_required
def get_barcode_value():
    filepath = request.args.get('filepath')
    if filepath == "":
        scan = scan_barcode_webcam(timeout_length=10)
    else:
        scan = scan_barcode_file(filepath)
    data = {'scan': scan}
    return jsonify(data)
