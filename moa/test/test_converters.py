"""test for group_manager"""
import xlrd
from matrix import Matrix, matrix_coordinates, col_to_num
from group_manager import GroupManager
from converters import XlsFile
import logging
import os
import sys
import unittest

# Go to upper directory and then import files
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
        pass

    def test_XlsFile(self):
        print("--- XlsFile() ---")
        xf = self.xf
        self.assertEqual(xf.name, "5-5")
        self.assertEqual(xf.coordinates, {'first_row': 1, 'last_row': 5,
                                          'first_col': 1, 'last_col': 5})
        self.assertEqual(xf.sheet_index, 0)

    # def test_parse(self):
    #     print("--- parse() ---")

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

        self.assertEqual(f, expected)

    def test_parse_cols(self):
        print("--- parse_cols() ---")
        ws = self.worksheet
        f = self.xf._parse_cols(ws)
        self.assertEqual(f, {
            "elma": [10.0, 0.0, 5.0, 14.0, 2.0],
            "ıspanak": [0.0, 12.0, 7.0, 3.0, 5.0],
            "armut": [5.0, 9.0, 6.0, 8.0, 9.0],
            "fasulye": [8.0, 3.0, 0.0, 7.0, 0.0],
            "muz": [1.0, 4.0, 11.0, 0.0, 5.0]})

    # def test_pop_row_name(self):
    #     print("--- pop_row() ---")

    # def test_pop_col_name(self):
    #     print("--- pop_col() ---")

    # def test_pop_row_val(self):
    #     print("--- pop_row_val() ---")

    # def test_pop_col_val(self):
    #     print("--- pop_col_val() ---")

    # def test_write(self):
    #     print("--- write() ---")

    # def test_get_order(self):
    #     print("--- get_order() ---")


if __name__ == "__main__":
    unittest.main()
