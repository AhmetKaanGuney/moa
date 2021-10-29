"""test for group_manager"""
from converters import Matrix
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

file_handler = logging.FileHandler(
    parentdir + "/moa/logs/grup_manager.log", mode="a", encoding=ENCODING
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


my_log = open(parentdir + "/moa/logs/engine_test.log", "w")
my_log.write("")
my_log.close()

source_matrix = Matrix(
    rows={
        "ali": [10.0, 0.0, 5.0, 8.0, 1.0],
        "esma": [0.0, 12.0, 9.0, 3.0, 4.0],
        "ahmet": [5.0, 7.0, 6.0, 0.0, 11.0],
        "ibrahim": [14.0, 3.0, 8.0, 7.0, 0.0],
        "derya": [2.0, 5.0, 9.0, 0.0, 5.0],
    },
    cols={
        "elma": [10.0, 0.0, 5.0, 14.0, 2.0],
        "ıspanak": [0.0, 12.0, 7.0, 3.0, 5.0],
        "armut": [5.0, 9.0, 6.0, 8.0, 9.0],
        "fasulye": [8.0, 3.0, 0.0, 7.0, 0.0],
        "muz": [1.0, 4.0, 11.0, 0.0, 5.0],
    },
)


user_row_groups = {"men": ["ali", "ahmet", "ibrahim"], "women": ["esma", "derya"]}
user_col_groups = {
    "vegetables": ["ıspanak", "fasulye"],
    "fruits": ["elma", "armut", "muz"],
}


class TestGroupManager(unittest.TestCase):
    def setUp(self):
        self.gm = GroupManager(source_matrix)
        self.gm.user_row_groups = user_row_groups
        self.gm.user_col_groups = user_col_groups

    def test_get_row_groups(self):
        print("--- get_row_groups() ---")
        self.assertEqual(self.gm.get_row_groups(), user_row_groups)

    def test_get_col_groups(self):
        print("--- get_col_groups() ---")
        self.assertEqual(self.gm.get_col_groups(), user_col_groups)

    def test_get_row_group(self):
        print("--- get_row_group() ---")
        self.assertEqual(self.gm.get_row_group("men"), user_row_groups["men"])

    def test_get_col_group(self):
        print("--- get_col_group() ---")
        print("gm col_group: ", self.gm.get_col_groups())
        print("user_col_groups: ", user_col_groups)
        self.assertEqual(self.gm.get_col_group("fruits"),
                         user_col_groups["fruits"])

    def test_create_row_group(self):
        print("--- create_row_group() ---")
        self.gm.create_row_group("test")
        urg = user_row_groups.copy()
        urg["test"] = []
        self.assertEqual(self.gm.user_row_groups, urg)
        del urg

    def test_create_col_gruop(self):
        print("--- create_col_group() ---")
        self.gm.create_col_group("test")
        ucg = user_col_groups.copy()
        ucg["test"] = []
        self.assertEqual(self.gm.user_col_groups, ucg)
        del ucg

    def test_add_rows_to_group(self):
        print("--- add_rows_to_group() ---")

    def test_add_cols_to_group(self):
        print("--- add_cols_to_group() ---")

    def test_convert_to_matrix(self):
        print("--- convert_to_matrix() ---")

    def test_sum_groups(self):
        print("--- sum_groups() ---")

    def test_sum_row_groups(self):
        print("--- sum_row_row_groups() ---")

    def test_sum_col_groups(self):
        print("--- sum_col_groups() ---")

    def test_build_with(self):
        print("--- build_with() ---")


if __name__ == "__main__":
    unittest.main()
