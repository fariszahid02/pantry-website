# Authored by: Joe
# This file contains tests for barcode_util.py
import cv2

from barcodes import barcode_util
import models
from unittest.mock import patch, MagicMock
import unittest
from app import create_app
from populate_db import create_barcodes, add_food_items


class TestBarcodeUtil(unittest.TestCase):

    def setUp(self) -> None:
        models.init_db()
        add_food_items()
        create_barcodes()

    def test_scan_barcode_file_with_code_present(self) -> None:
        code_list = [barcode_util.scan_barcode_file("barcodes/barcode_test_data/barcode_sample_1.png"),
                     barcode_util.scan_barcode_file("barcodes/barcode_test_data/barcode_sample_2.webp"),
                     barcode_util.scan_barcode_file("barcodes/barcode_test_data/barcode_sample_3.jfif"),
                     barcode_util.scan_barcode_file("barcodes/barcode_test_data/barcode_sample_4.jpg"),
                     barcode_util.scan_barcode_file("barcodes/barcode_test_data/barcode_sample_5.jpg")]
        expected = ["0512345000107", "9300633929169", "23987234987", "5022032139942", "6971958734962"]
        self.assertEqual(expected, code_list, msg="Barcodes read incorrectly")

    def test_scan_barcode_file_with_code_absent(self) -> None:
        self.assertIsNone(barcode_util.scan_barcode_file("barcodes/barcode_test_data/absent_barcode_sample.jpg"),
                          msg="Barcodes read incorrectly")

    def test_scan_barcode_file_with_invalid_filetype(self) -> None:
        self.assertIsNone(barcode_util.scan_barcode_file("barcodes/barcode_test_data/text_file.txt"),
                          msg="Barcodes read incorrectly")

    @patch('cv2.VideoCapture')
    def test_scan_barcode_webcam(self, mock_VideoCapture):
        # Mock VideoCapture object
        mock_capture = MagicMock()
        mock_VideoCapture.return_value = mock_capture

        # Simulate webcam frame
        frame = cv2.imread("barcodes/barcode_test_data/barcode_sample_1.png")
        mock_capture.read.side_effect = [(True, frame), (True, frame), (True, frame)]

        result = barcode_util.scan_barcode_webcam(timeout_length=0.5)
        self.assertEqual(result, '0512345000107')

        mock_capture.release.assert_called_once()
        cv2.destroyAllWindows()

    @patch('cv2.VideoCapture')
    def test_scan_barcode_webcam_absent(self, mock_VideoCapture):
        # Mock VideoCapture object
        mock_capture = MagicMock()
        mock_VideoCapture.return_value = mock_capture

        # Simulate webcam frame
        frame = cv2.imread("barcodes/barcode_test_data/absent_barcode_sample.jpg")
        mock_capture.read.side_effect = [(True, frame)] * 200

        result = barcode_util.scan_barcode_webcam(timeout_length=0.5)
        self.assertIsNone(result)

        mock_capture.release.assert_called_once()
        cv2.destroyAllWindows()

    def test_create_barcode(self) -> None:
        # create the barcode
        barcode_util.create_barcode(barcode="189328752815", food_name="White Rice", quantity=5, units="kg")

        # query the created barcode
        created_barcode = models.Barcode.query.filter_by(barcode="189328752815").first()

        # Check barcode fields are as they should be
        self.assertEqual(created_barcode.barcode, "189328752815")
        self.assertEqual(created_barcode.get_name(), "White Rice")
        self.assertEqual(created_barcode.get_quantity(), 5.0)
        self.assertEqual(created_barcode.get_units(), "kg")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        unittest.main(exit=False)
