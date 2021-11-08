"""test for group_manager"""
# import logging
import os
import unittest

from converters import Matrix
from group_manager import GroupManager

source_matrix = Matrix(
    rows={
        "ali": [10.0, 0.0, 5.0, 8.0, 1.0, 50],
        "esma": [0.0, 12.0, 9.0, 3.0, 4.0, 50],
        "ahmet": [5.0, 7.0, 6.0, 0.0, 11.0, 50],
        "ibrahim": [14.0, 3.0, 8.0, 7.0, 0.0, 50],
        "derya": [2.0, 5.0, 9.0, 0.0, 5.0, 50],
        "sr1": [100, 100, 100, 100, 100, 150],
    },
    cols={
        "elma": [10.0, 0.0, 5.0, 14.0, 2.0, 100],
        "ıspanak": [0.0, 12.0, 7.0, 3.0, 5.0, 100],
        "armut": [5.0, 9.0, 6.0, 8.0, 9.0, 100],
        "fasulye": [8.0, 3.0, 0.0, 7.0, 0.0, 100],
        "muz": [1.0, 4.0, 11.0, 0.0, 5.0, 100],
        "sc1": [50, 50, 50, 50, 50, 150],
    },
)

expected_matrix = Matrix(
    rows={"men": [60, 25], "women": [29, 20],},
    cols={"fruits": [60, 29], "vegetables": [25, 20]},
)

user_row_groups = {"men": ["ali", "ahmet", "ibrahim"],
                   "women": ["esma", "derya"]}
user_col_groups = {
    "fruits": ["elma", "armut", "muz"],
    "vegetables": ["ıspanak", "fasulye"]}


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
        self.assertEqual(self.gm.get_col_group("fruits"), user_col_groups["fruits"])

    def test_create_row_group(self):
        print("--- create_row_group() ---")
        urg = user_row_groups.copy()
        urg["test"] = []
        self.gm.create_row_group("test")
        self.assertEqual(self.gm.user_row_groups, urg)

    def test_create_col_group(self):
        print("--- create_col_group() ---")
        ucg = user_col_groups.copy()
        ucg["test"] = []
        self.gm.create_col_group("test")
        self.assertEqual(self.gm.user_col_groups, ucg)

    def test_add_rows_to_group(self):
        print("--- add_rows_to_group() ---")
        self.gm.add_rows_to_group(["sr1"], "men")
        self.assertEqual(
            self.gm.user_row_groups["men"], ["ali", "ahmet", "ibrahim", "sr1"]
        )

    def test_add_cols_to_group(self):
        print("--- add_cols_to_group() ---")
        self.gm.add_cols_to_group(["sc1"], "vegetables")
        self.assertEqual(
            self.gm.user_col_groups["vegetables"], ["ıspanak", "fasulye", "sc1"]
        )


    def test_convert_to_matrix(self):
        print("--- convert_to_matrix() ---")
        self.gm.user_row_groups["men"].remove("sr1")
        self.gm.user_col_groups["vegetables"].remove("sc1")
        print()
        print("BEFORE Covert: ")
        print(f"{self.gm.user_row_groups=}")
        print(f"{self.gm.user_col_groups=}\n")
        output_matrix = self.gm.convert_to_matrix()

        print(f"{output_matrix.rows=}")
        print(f"{output_matrix.cols=}\n")
        print(f"{expected_matrix.rows=}")
        print(f"{expected_matrix.cols=}\n")

        self.assertDictEqual(output_matrix.rows, expected_matrix.rows)
        self.assertDictEqual(output_matrix.cols, expected_matrix.cols)

    # def test_sum_groups(self):
    #     print("--- sum_groups() ---")

    # def test_sum_row_groups(self):
    #     print("--- sum_row_groups() ---")

    # def test_sum_col_groups(self):
    #     print("--- sum_col_groups() ---")

    # def test_build_with(self):
    #     print("--- build_with() ---")


if __name__ == "__main__":
    print("CWD: ", os.getcwd())
    unittest.main()

