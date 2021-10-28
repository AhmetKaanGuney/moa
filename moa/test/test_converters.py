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
        workbook = xlrd.open_workbook(file_path,
                                           encoding_override=ENCODING, 
                                           on_demand=True)
        self.worksheet = workbook.sheet_by_index(self.sheet_index)

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
        self.assertEqual(f, {
            "ali": [10, 0, 5, 8, 1],
            "esma": [0, 12, 9, 3, 4],
            "ahmet": [5, 7, 6, 0, 11],
            "ibrahim": [14, 3, 8, 7, 0],
            "derya": [2, 5, 9, 0, 5]})

    def test_parse_cols(self):
        print("--- parse_cols() ---")
        ws = self.worksheet
        f = self.xf._parse_rows(ws)
        self.assertEqual(f, {
            "elma": [10, 0, 5, 8, 1],
            "ıspanak": [0, 12, 9, 3, 4],
            "armut": [5, 7, 6, 0, 11],
            "fasulye": [14, 3, 8, 7, 0],
            "muz": [2, 5, 9, 0, 5]})

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
