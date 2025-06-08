# Authored by: Joe
# This file contains functions to read and write barcodes
import cv2
from pyzbar.pyzbar import decode
import datetime
from app import db
from models import Barcode, QuantifiedFoodItem, create_or_get_food_item, create_and_get_qfid


def scan_barcode_webcam(timeout_length):

    # Get webcam capture
    capture = cv2.VideoCapture(0)

    start_time = datetime.datetime.now()
    barcodes = []

    while capture.isOpened():
        # Read current frame from webcam
        success, frame = capture.read()
        # Flip frame for scanning barcode
        frame = cv2.flip(frame, 1)
        # Get barcode from frame
        detected_barcode = decode(frame)
        if not detected_barcode:
            # Exit function if no barcode detected within specified time
            if (datetime.datetime.now()-start_time).total_seconds() >= timeout_length:
                capture.release()
                cv2.destroyAllWindows()
                return None
        else:
            for barcode in detected_barcode:
                if barcode.data != "":
                    barcodes.append(barcode.data)
                    # Check that barcode has been read as the same value consecutively 3 times to prevent a misread.
                    if len(barcodes) >= 3:
                        if barcodes[-1] == barcodes[-2] and barcodes[-2] == barcodes[-3]:
                            capture.release()
                            cv2.destroyAllWindows()
                            return barcode.data.decode()
        cv2.imshow("barcode capture - press 'e' to exit", frame)
        if cv2.waitKey(1) == ord('e'):
            break
    capture.release()
    cv2.destroyAllWindows()
    return None


def scan_barcode_file(filepath):
    # read image from specified filepath
    frame = cv2.imread(filepath)
    if frame is None:
        return None
    # get barcode from image
    detected_barcode = decode(frame)
    if not detected_barcode:
        # exit function if no barcode detected
        return None
    else:
        for barcode in detected_barcode:
            if barcode.data != "":
                return barcode.data.decode()


def create_barcode(barcode, food_name, quantity, units):
    food_item = create_or_get_food_item(food_name)
    qfood_id = create_and_get_qfid(food_id=food_item.id, quantity=float(quantity), units=units)
    barcode_item = Barcode(qfood_id, barcode)
    db.session.add(barcode_item)
    db.session.commit()
