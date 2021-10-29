"""test for group_manager"""
import xlrd
from matrix import Matrix, matrix_coordinates
from converters import XlsFile
import logging
import os
import sys
import unittest

cwd = os.getcwd()
parentdir = os.path.dirname(cwd)
sys.path.append(parentdir)
print("parent dir: ", parentdir)


ENCODING = "UTF-8"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(message)s")

file_handler = logging.FileHandler(parentdir + "/moa/logs/converters.log",
                                   mode="a", encoding=ENCODING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


try:
    my_log = open(parentdir + "/moa/logs/converters.log", "w")
    my_log.write("")
    my_log.close()
except FileNotFoundError:
    pass

FIRST_ROW_NAME = "ali"
FIRST_COL_NAME = "elma"
TOP_LEFT_CORNER_VALUE = 10
BOTTOM_RIGHT_CORNER_VALUE = 5
OUTPUT_PATH = parentdir + "/moa/test/output_files/test.xls"
MATRIX = Matrix(rows={
            "ali": [10.0, 0.0, 5.0, 8.0, 1.0],
            "esma": [0.0, 12.0, 9.0, 3.0, 4.0],
            "ahmet": [5.0, 7.0, 6.0, 0.0, 11.0],
            "ibrahim": [14.0, 3.0, 8.0, 7.0, 0.0],
            "derya": [2.0, 5.0, 9.0, 0.0, 5.0]},
            cols={
            "elma": [10.0, 0.0, 5.0, 14.0, 2.0],
            "ıspanak": [0.0, 12.0, 7.0, 3.0, 5.0],
            "armut": [5.0, 9.0, 6.0, 8.0, 9.0],
            "fasulye": [8.0, 3.0, 0.0, 7.0, 0.0],
            "muz": [1.0, 4.0, 11.0, 0.0, 5.0]})


class TestXlsFile(unittest.TestCase):

    def setUp(self):
        file_path = parentdir + "/moa/test/input_files/5-5.xls"
        matrix_coords = matrix_coordinates((2, 6), ("B", "F"))
        self.xf = XlsFile(file_path, matrix_coords)
        self.workbook = xlrd.open_workbook(file_path,
                                           encoding_override=ENCODING,
                                           on_demand=True)
        self.worksheet = self.workbook.sheet_by_index(self.xf.sheet_index)

    def tearDown(self) -> None:
        self.workbook.release_resources()
        del self.workbook

    def test_XlsFile(self):
        print("--- XlsFile() ---")
        xf = self.xf
        self.assertEqual(xf.name, "5-5")
        self.assertEqual(xf.coordinates, {'first_row': 1, 'last_row': 5,
                                          'first_col': 1, 'last_col': 5})
        self.assertEqual(xf.sheet_index, 0)

    def test_parse(self):
        print("--- parse() ---")
        test_matrix = self.xf.parse()
        self.assertDictEqual(test_matrix.rows, MATRIX.rows)
        self.assertDictEqual(test_matrix.cols, MATRIX.cols)

    def test_parse_rows(self):
        print("--- parse_rows() ---")
        ws = self.worksheet
        f = self.xf._parse_rows(ws)
        expected = {
            "ali": [10.0, 0.0, 5.0, 8.0, 1.0],
            "esma": [0.0, 12.0, 9.0, 3.0, 4.0],
            "ahmet": [5.0, 7.0, 6.0, 0.0, 11.0],
            "ibrahim": [14.0, 3.0, 8.0, 7.0, 0.0],
            "derya": [2.0, 5.0, 9.0, 0.0, 5.0]}

        self.assertDictEqual(f, expected)

    def test_parse_cols(self):
        print("--- parse_cols() ---")
        ws = self.worksheet
        f = self.xf._parse_cols(ws)
        self.assertDictEqual(f, {
            "elma": [10.0, 0.0, 5.0, 14.0, 2.0],
            "ıspanak": [0.0, 12.0, 7.0, 3.0, 5.0],
            "armut": [5.0, 9.0, 6.0, 8.0, 9.0],
            "fasulye": [8.0, 3.0, 0.0, 7.0, 0.0],
            "muz": [1.0, 4.0, 11.0, 0.0, 5.0]})

    def test_pop_row_name(self):
        print("--- pop_row() ---")
        first_row = self.xf.coordinates["first_row"]
        # This is how it's implemented at _parse_rows() function
        first_col = self.xf.coordinates["first_col"] - 1
        ws = self.worksheet
        rowx = first_row
        start_colx = first_col
        f = self.xf._pop_row_name(ws, rowx, start_colx)
        self.assertEqual(f, FIRST_ROW_NAME)

    def test_pop_col_name(self):
        print("--- pop_col() ---")
        first_col = self.xf.coordinates["first_col"]
        # This is how it's implemented at _parse_rows() function
        first_row = self.xf.coordinates["first_row"] - 1
        ws = self.worksheet
        start_rowx = first_row
        colx = first_col
        f = self.xf._pop_col_name(ws, colx, start_rowx)
        self.assertEqual(f, FIRST_COL_NAME)

    def test_pop_row_val(self):
        print("--- pop_row_val() ---")
        first_row = self.xf.coordinates["first_row"]
        # This is how it's implemented at _parse_rows() function
        first_col = self.xf.coordinates["first_col"]
        ws = self.worksheet
        rowx = first_row
        start_colx = first_col
        f = self.xf._pop_row_val(ws, rowx, start_colx)
        self.assertEqual(f, TOP_LEFT_CORNER_VALUE)

    def test_pop_col_val(self):
        print("--- pop_col_val() ---")
        last_row = self.xf.coordinates["last_row"]
        # This is how it's implemented at _parse_rows() function
        last_col = self.xf.coordinates["last_col"]
        ws = self.worksheet
        colx = last_col
        start_rowx = last_row
        f = self.xf._pop_col_val(ws, colx, start_rowx)
        self.assertEqual(f, BOTTOM_RIGHT_CORNER_VALUE)

    def test_write(self):
        print("--- write() ---")
        self.xf.write(OUTPUT_PATH, MATRIX)


if __name__ == "__main__":
    unittest.main()
