"""Format convertors"""
import json

import pandas as pd
import xlrd
import xlwt

from .matrix import Matrix
from .errors import DuplicationError, EmptyError, Error, NaNError

# For Tesing import these
# import matrix
# from errors import DuplicationError, EmptyError, Error, NaNError
# from matrix import Matrix

ENCODING = "UTF-8"


def json_to_matrix(json_string):
    js = json.loads(json_string)
    rows = js["rows"]
    cols = js["cols"]
    return Matrix(rows=rows, cols=cols)


def matrix_to_json(matrix: Matrix):
    rows = matrix.rows
    cols = matrix.cols
    return json.dumps({"rows": rows, "cols": cols})


def get_order(num):
    """Returns number in string with order attached"""
    div = num
    n = 0
    while div > 1:
        div = round(div / 10)
        n += 1

    remainder = num % 10
    s_num = str(num)
    last_two_digits = num % 100
    if 10 < last_two_digits < 20:
        return s_num + "th"
    if remainder == 1:
        return s_num + "st"
    if remainder == 2:
        return s_num + "nd"
    if remainder == 3:
        return s_num + "rd"
    # else
    return s_num + "th"


class XlsFile:
    """This class is for reading and writing XLS files.
    It takes file_path's path, the coordinates and sheet_index of the
    excel file_path as arguments.
    The coordinates:  are needed for deciding the start and end places of the
    parsing.
    Sheet index: is for which sheet to read from in the excel"""

    def __init__(
        self, matrix_coords: dict, file_path="", file_stream=b"", sheet_index=0
    ):
        self.file_path = file_path
        self.file_stream = file_stream
        self.coordinates = matrix_coords
        self.sheet_index = sheet_index

        self.first_row, self.last_row = (
            matrix_coords["first_row"],
            matrix_coords["last_row"],
        )
        self.first_col, self.last_col = (
            matrix_coords["first_col"],
            matrix_coords["last_col"],
        )
        self.rows_skipped, self.cols_skipped = 0, 0

        self.row_names = []
        self.col_names = []

        x_length = self.x_length = (self.last_row - self.first_row) + 1
        y_length = self.y_length = (self.last_col - self.first_col) + 1
        self.size = (x_length, y_length)

    # ----------------------- #
    #         PARSER          #
    # ----------------------- #

    def parse(self):
        """- parses rows then cols
        - returns Matrix() object"""
        if self.file_path:
            workbook = xlrd.open_workbook(
                self.file_path, encoding_override=ENCODING, on_demand=True
            )
        elif self.file_stream:
            try:
                workbook = xlrd.open_workbook(
                    file_contents=self.file_stream,
                    encoding_override=ENCODING,
                    on_demand=True,
                )
            except Exception:
                Error.set_message(
                    "An error occured while reading the file.\nThe file might corrupted or you might have entered wrong coordinates for the matrix."
                )
                return None
        worksheet = workbook.sheet_by_index(self.sheet_index)

        try:
            rows = self._parse_rows(worksheet)
            cols = self._parse_cols(worksheet)
        except Error:
            self.dump_workbook(workbook)
            return None
        except IndexError:
            Error.set_message("Invalid matrix coordinates.")
            self.dump_workbook(workbook)
            return None

        self.dump_workbook(workbook)
        return Matrix(rows=rows, cols=cols)

    def _parse_rows(self, worksheet):
        """The names of the rows are read vertically. The values of rows are read horizontally.
        So the first iteration is vertical and the second iteration is horizontal.
            -returns dictionary: {'row': [val1, val2, ...]}"""
        first_row, last_row = self.first_row, self.last_row
        first_col, last_col = self.first_col, self.last_col

        rows = {}
        empty_row_index = 1  # tracking this for empty row error

        # Vertical Iteration / get rows' name
        the_column_which_has_all_rows_names = (
            self.first_col - 1
        )  # This is the cols that has rows' names
        # Added 1 otherwise it isn't inclusive
        for each_row in range(first_row, last_row + 1):
            row_name = self._pop_row_name(
                worksheet, rowx=each_row, start_colx=the_column_which_has_all_rows_names
            )
            row_vals = []  # reset the values for each rows

            if row_name != "":
                # Horizontal Iteration / get rows' values
                for each_col in range(first_col, last_col + 1):
                    value_of_each_column = self._pop_col_val(
                        worksheet, colx=each_col, start_rowx=each_row
                    )
                    row_vals.append(value_of_each_column)

                rows[row_name] = row_vals
                empty_row_index += 1
            else:
                raise EmptyError(
                    f"{get_order(empty_row_index)} row is empty!"
                    f"Make sure there are no gaps between rows."
                )
        return rows

    def _parse_cols(self, worksheet):
        """The names of the cols are read horizontally. The values of cols
        are read vertically.
        The first iteration is horizontal. The second iteration is vertical.
        :returns dictionary{'col': [val1, val2, ...]}"""
        first_row, last_row = self.first_row, self.last_row
        first_col, last_col = self.first_col, self.last_col

        cols = {}
        empty_col_index = 1  # tracking this for empty col error

        the_row_which_has_all_cols_names = (
            first_row - 1
        )  # This is the rows that has the cols' names

        # Horizontal Iteration / get cols' name
        # Added 1 otherwise it isn't inclusive
        for each_col in range(first_col, last_col + 1):
            col_name = self._pop_col_name(
                worksheet, colx=each_col, start_rowx=the_row_which_has_all_cols_names
            )
            col_vals = []  # reset the values for each cols

            if col_name != "":
                # Vertical Iteration / get cols' values
                for each_row in range(first_row, last_row + 1):
                    value_of_each_row = self._pop_row_val(
                        worksheet, rowx=each_row, start_colx=each_col
                    )
                    col_vals.append(value_of_each_row)

                empty_col_index += 1
                cols[col_name] = col_vals
            else:
                raise EmptyError(
                    f"{get_order(empty_col_index)} column is empty! "
                    f"Make sure there are no gaps between columns."
                )
        return cols

    def _pop_row_name(self, worksheet, rowx, start_colx):
        """Keeps track of the row names. Raises error if there is a duplicate name.
        - returns: the name of the row"""
        row_vals = worksheet.row_values(
            rowx=rowx, start_colx=start_colx
        )  # list has only 1 item in it
        name = row_vals.pop(0)  # remove brackets from value
        if name in self.row_names:
            raise DuplicationError(
                f"Duplication of '{name}' detected in row names."
                f"Make sure that all row names are unique."
            )
        else:
            self.row_names.append(name)
            return name

    def _pop_col_name(self, worksheet, colx, start_rowx):
        """Keeps track of the col names. Raises if there's a duplicate name.
        - returns: the name of the col"""
        col_vals = worksheet.col_values(
            colx=colx, start_rowx=start_rowx
        )  # list has only 1 item in it
        name = col_vals.pop(0)  # remove brackets from value
        if name in self.col_names:
            raise DuplicationError(
                f"Duplication of '{name}' detected in column names."
                f"Make sure that all column names are unique."
            )
        else:
            self.col_names.append(name)
            return name

    @staticmethod
    def _pop_row_val(worksheet, rowx, start_colx):
        """Checks the type of the value inside the cell. Raises error if value is NaN.
        - returns: the value of cell"""
        row_vals = worksheet.row_values(
            rowx=rowx, start_colx=start_colx  # list has only 1 item in it
        )
        value = row_vals.pop(0)  # remove brackets from value
        # type check
        if type(value) == int or float or None:
            return value
        else:
            raise NaNError(
                f"Cell ({rowx}, {start_colx}) does not contain number value."
                "Make sure that all cells contain a number value."
            )

    @staticmethod
    def _pop_col_val(worksheet, colx, start_rowx):
        """Checks the type of the value inside the cell. Raises error if value is NaN.
        - returns: the value of cell"""
        col_vals = worksheet.col_values(
            colx=colx, start_rowx=start_rowx  # list has only 1 item in it
        )
        value = col_vals.pop(0)  # remove brackets from value
        if type(value) in (int, float, None):
            return value
        else:
            raise NaNError(
                f"Cell ({start_rowx}, {colx}) does not contain number value."
                "Make sure that all cells contain a number value."
            )

    # ----------------------- #
    #         WRITER          #
    # ----------------------- #
    @staticmethod
    def write(file_path: str, matrix: Matrix):
        """Writes the given matrix to an xls file_path.
        :param file_path: where to store the file_path
        :param matrix: Matrix() object that has the row and col data"""
        workbook = xlwt.Workbook(encoding=ENCODING)
        worksheet = workbook.add_sheet("Sheet 0")
        excel_file_path = file_path

        # Write Row, Col Names
        row_names = matrix.get_rows()
        col_names = matrix.get_cols()
        row_len = len(row_names)
        col_len = len(col_names)

        # write row names
        for i in range(0, row_len):
            worksheet.write(i + 1, 0, row_names[i])

        # write col_names
        for i in range(0, col_len):
            worksheet.write(0, i + 1, col_names[i])

        # Write DATA
        for r in range(0, row_len):
            for c in range(0, col_len):
                row_name = row_names[r]
                col_name = col_names[c]
                data_val = matrix.get_cell(row_name, col_name)
                worksheet.write(r + 1, c + 1, data_val)

        workbook.save(excel_file_path)

    @staticmethod
    def dump_workbook(workbook):
        """Deletes workbook"""
        workbook.release_resources()
        del workbook


class XlsxFile:
    def __init__(self, matrix_coords: dict, file_path="", file_stream="b"):
        self.file_path = file_path
        self.file_stream = file_stream
        self.coordinates = matrix_coords

        self.first_row, self.last_row = (
            matrix_coords["first_row"],
            matrix_coords["last_row"],
        )
        self.first_col, self.last_col = (
            matrix_coords["first_col"],
            matrix_coords["last_col"],
        )

    # ----------------------- #
    #         PARSER          #
    # ----------------------- #
    def parse(self) -> Matrix:
        "returns: Matrix() object"
        if self.file_path:
            df = pd.read_excel(
                self.file_path,
                index_col=0,
                usecols=list(range(self.first_col - 1, self.last_col + 1)),
                skiprows=self.first_row - 1,
            )
        elif self.file_stream:
            df = pd.read_excel(
                self.file_stream,
                index_col=0,
                usecols=list(range(self.first_col - 1, self.last_col + 1)),
                skiprows=self.first_row - 1,
            )
        # Autofill empty cells with 0
        df.fillna(0, inplace=True, axis=0)

        rows = {}
        cols = {}

        # Generate rows
        for i, r in enumerate(df.index):
            row_vals = list(df.loc[r])
            rows[r] = row_vals

        # Generate cols
        for i, c in enumerate(df):
            col_vals = list(df[c])
            cols[c] = col_vals

        # Check for name values
        for i, duplicating in enumerate(list(df.index.duplicated())):
            if duplicating == True:
                raise DuplicationError(
                        f"Duplication of '{df.index[i]}' detected in row names."
                        f"Make sure that all column names are unique."
                )

        self.check_names(rows.keys(), "row")
        self.check_names(cols.keys(), "column")

        # Check for values
        for i, r in enumerate(rows):
            self.check_values(rows[r], i, "row")

        for i, c in enumerate(cols):
            self.check_values(cols[c], i, "column")

        # return Matrix() object
        return Matrix(rows, cols)

    # ----------------------- #
    #         WRITER          #
    # ----------------------- #
    @staticmethod
    def write(file_path: str, processed_matrix: Matrix):
        index_names = processed_matrix.get_rows()
        data = processed_matrix.cols
        df = pd.DataFrame(data=data, index=index_names)

        pd.DataFrame.to_excel(df, excel_writer=file_path)


    @staticmethod
    def check_names(names, row_or_col):
        found = []
        for i, name in enumerate(names):
            name = str(name)
            # Check if name is 'nan'
            if name in ("nan", "0"):
                raise EmptyError(
                    f"{get_order(i + 1)} {row_or_col} is empty!"
                    f"Make sure there are no gaps between {row_or_col}s."
                )
            # Check if name is "Unnamed"
            if "Unnamed: " in name:
                raise EmptyError(
                    f"{get_order(i + 1)} {row_or_col} is empty!"
                    f"Make sure there are no gaps between {row_or_col}s."
                )
            # Check if name has a duplicate
            if name in found:
                simple_name = name.split(".")[0]
                raise DuplicationError(
                    f"Duplication of '{simple_name}' detected in {row_or_col} names."
                    f"Make sure that all column names are unique."
                )
            else:
                found.append(name)
                found.append(name + ".1")

    @staticmethod
    def check_values(values, index, row_or_col):
        for i, v in enumerate(values):
            # print(f"{v}", type(v))
            if type(v) is str:
                if row_or_col == "row":
                    coordinate = f"{index + 1}, {i + 1}"
                else:
                    coordinate = f"{i + 1}, {index + 1}"
                raise NaNError(
                    f"Cell at ({coordinate}) does not contain number value."
                    "Make sure that all cells contain a number value."
                )


if __name__ == "__main__":
    print("--- TESTING converters.py ---")
    # TEST
    # mc = matrix.coordinates(rows=(2, 7), cols=("b", "g"))
    # mc = matrix.coordinates(rows=(11, 16), cols=("f", "k"))
    # f = XlsxFile(mc, "./test/input_files/xlsx/5-5.xlsx")
    # f = XlsxFile(mc, "./test/input_files/xlsx/5-5_row_name_duplication.xlsx")
    # f = XlsxFile(mc, "./test/input_files/xlsx/5-5_col_name_duplication.xlsx")
    # f = XlsxFile(mc, "./test/input_files/xlsx/5-5_empty_cell.xlsx")
    # f = XlsxFile(mc, "./test/input_files/xlsx/5-5_empty_col.xlsx")
    # f = XlsxFile(mc, "./test/input_files/xlsx/5-5_empty_row.xlsx")
    # f = XlsxFile(mc, "./test/input_files/xlsx/5-5_nan_cell.xlsx")
    # result_matrix = f.parse()
    # print(result_matrix)
    # processed_matrix = Matrix(rows={
    #         "ali": [10.0, 0.0, 5.0, 8.0, 1.0],
    #         "esma": [0.0, 12.0, 9.0, 3.0, 4.0],
    #         "ahmet": [5.0, 7.0, 6.0, 0.0, 11.0],
    #         "ibrahim": [14.0, 3.0, 8.0, 7.0, 0.0],
    #         "derya": [2.0, 5.0, 9.0, 0.0, 5.0]},
    #         cols={
    #         "elma": [10.0, 0.0, 5.0, 14.0, 2.0],
    #         "ıspanak": [0.0, 12.0, 7.0, 3.0, 5.0],
    #         "armut": [5.0, 9.0, 6.0, 8.0, 9.0],
    #         "fasulye": [8.0, 3.0, 0.0, 7.0, 0.0],
    #         "muz": [1.0, 4.0, 11.0, 0.0, 5.0]})
    # XlsxFile.write("./TEST.xlsx", processed_matrix)
