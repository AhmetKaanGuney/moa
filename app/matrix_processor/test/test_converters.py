"""test for group_manager"""
import xlrd
import os
import unittest

from converters import XlsFile
from matrix import Matrix, matrix_coordinates


ENCODING = "utf-8"
FIRST_ROW_NAME = "ali"
FIRST_COL_NAME = "elma"
TOP_LEFT_CORNER_VALUE = 10
BOTTOM_RIGHT_CORNER_VALUE = 5
INPUT_PATH = os.getcwd() + "/test/input_files/5-5.xls"
OUTPUT_PATH = os.getcwd() + "/test/output_files/test.xls"
print(f"{OUTPUT_PATH=}")
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
        matrix_coords = matrix_coordinates((2, 6), ("B", "F"))
        self.xf = XlsFile(INPUT_PATH, matrix_coords)
        self.workbook = xlrd.open_workbook(INPUT_PATH,
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
    print("CWD: ", os.getcwd())
    unittest.main()
