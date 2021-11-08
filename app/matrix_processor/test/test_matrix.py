"""test for matrix"""
import os
import unittest

from converters import Matrix
#  TODO FIX SUMS add sums to sr1 and sc1

source_rows = {
        "ali": [10.0, 0.0, 5.0, 8.0, 1.0, 50],
        "esma": [0.0, 12.0, 9.0, 3.0, 4.0, 50],
        "ahmet": [5.0, 7.0, 6.0, 0.0, 11.0, 50],
        "ibrahim": [14.0, 3.0, 8.0, 7.0, 0.0, 50],
        "derya": [2.0, 5.0, 9.0, 0.0, 5.0, 50],
        "sr1": [100, 100, 100, 100, 100, 150]}

source_cols = {
        "elma": [10.0, 0.0, 5.0, 14.0, 2.0, 100],
        "ıspanak": [0.0, 12.0, 7.0, 3.0, 5.0, 100],
        "armut": [5.0, 9.0, 6.0, 8.0, 9.0, 100],
        "fasulye": [8.0, 3.0, 0.0, 7.0, 0.0, 100],
        "muz": [1.0, 4.0, 11.0, 0.0, 5.0, 100],
        "sc1": [50, 50, 50, 50, 50, 150]
    }

source_matrix = Matrix(rows=source_rows, cols=source_cols)

summed_matrix = Matrix(
    rows={
        "men": [60, 25],
        "women": [29, 20],
    },
    cols={
        "vegetables": [25, 20],
        "fruits": [60, 29]
    }
    )

men_sum = [29,10,19,15,12]
fruits_sum = [2,17,18,3,9]

class TestMatrix(unittest.TestCase):
    def setUp(self) -> None:
        self.sm = source_matrix

    def test_get_rows(self):
        rows = self.sm.get_rows()
        self.assertEqual(rows, list(source_rows.keys()))

    def test_get_cols(self):
        cols = self.sm.get_cols()
        self.assertEqual(cols, list(source_cols.keys()))

    def test_get_cell(self):
        cell = self.sm.get_cell("ali", "elma")
        self.assertEqual(cell, 10)

    def test_get_row(self):
        self.assertEqual(self.sm.get_row("ali"), source_rows["ali"])

    def test_get_col(self):
        self.assertEqual(self.sm.get_col("elma"), source_cols["elma"])

    def test_sum_rows(self):
        output = self.sm.sum_rows(["ali", "ahmet", "ibrahim"])
        self.assertEqual(output, men_sum)

    def test_sum_cols(self):
        output = self.sm.sum_cols(["elma", "armut", "muz"])
        self.assertEqual(output, fruits_sum)

if __name__ == "__main__":
    print("CWD: ", os.getcwd())
    unittest.main()