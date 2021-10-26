import logging
import xlrd

ENCODING = "UTF-8"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(message)s")
file_handler = logging.FileHandler("../test/logs/test.log", mode="w", encoding=ENCODING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Summary of the PARSER : Input-> data_file >>> Output-> 2 lists (rows and columns)
#
# The function of the PARSER is:
# - Get inputted data file_path's format
# - If program supports the format:
#   - Get groups from file_path (according to it's format)
#   - Convert each rows and column to a dictionary
#   - Make a list of rows
#   - Make a list of columns
#   - Return : rows and cols
#
# Then the Matrix object takes these two lists as it's arguments

# Make a script for file_path format
# if it's in csv format use csv_parser(file_path)
# if it's ni xls format use xls_parser(file_path)
# make a function that takes a file_path in a supported format
# that reads the file_path and returns 2 lists
def get_order(num):
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


# ------------------------ #
#     Column to Number     #
# ------------------------ #
def col_to_num(col):
    num = 0
    for c in col:
        num = num * 26 + (ord(c.upper()) - ord('A')) + 1
        #       0       +    (65  -  65) + 1
        # this num*26 let's the second character to skip all single letters and get it's own value
    return num


# ------------------------ #
#       Coordinates        #
# ------------------------ #
def matrix_coordinates(rows: tuple, cols: tuple):
    """You can think of the Matrix as a rectangle. The parser needs to know all the four coordinates.\n
    Every value is subtracted by 1 so user can enter what is shown on the Excel groups. \n
    Then the program adjusts these values to be compatible with zero indexing.
    :param rows (first_row, last_row) >> takes int
    :param cols (first_col, last_col) >> takes string
    :returns dictionary
    """
    f_row, l_row = rows[0] - 1, rows[1] - 1

    # col_tup[0] = 'A' >>> 'A' == 1 >>> returns 'A' - 1
    f_col, l_col = col_to_num(cols[0]) - 1, col_to_num(cols[1]) - 1

    coord = {"first_row": f_row, "last_row": l_row, "first_col": f_col, "last_col": l_col}
    logger.debug(f" Returning coordinates. \n"
                 f"\t- first_row : {coord['first_row']}\n"
                 f"\t- last_row : {coord['last_row']}\n"
                 f"\t- first_col : {coord['first_col']}\n"
                 f"\t- last_col : {coord['last_col']}")
    return coord


# -----------------------  #
#         MATRIX           #
# -----------------------  #
class Matrix:
    """Every Matrix() object has these attributes:
    - name : name of the Matrix()
    - rows : a dict that has rows names as keys and lists as their values
    - cols : a dict that has cols name as keys and lists as their values
    - """

    def __init__(self, name: str, rows: dict, cols: dict):
        self.name = name
        self.rows = rows
        self.cols = cols

    # ----------------- #
    #    GET METHODS    #
    # ----------------- #
    def get_cell(self, row_name: str, col_name: str):
        i = 0
        # Vertical iteration
        for col in self.cols:
            if col == col_name:
                break
            i += 1
        cell = self.rows[row_name][i]
        logger.info(f" {self.name}:\tCell:\t({row_name}, {col_name}):\t{cell}")
        return cell

    def get_rows(self):
        """returns: all of the rows' name in a list"""
        row_names = []
        for name in self.rows.keys():
            row_names.append(name)

        logger.info(f" {self.name}:\tRows:\t{row_names}")
        return row_names

    def get_cols(self):
        """returns: all of the cols' name in a list"""
        col_names = []
        for name in self.cols.keys():
            col_names.append(name)

        logger.info(f" {self.name}:\tCols:\t{col_names}")
        return col_names

    def get_row(self, name: str):
        logger.info(f" Row: '{name}'\t:\t{self.rows[name]}")
        return self.rows[name]

    def get_col(self, name: str):
        logger.info(f" Col: '{name}'\t:\t{self.cols[name]}")
        return self.cols[name]

    # ------------------------ #
    #    ADD/REMOVE METHODS    #
    # ------------------------ #
    def sum_of_rows(self, row1: str, row2: str):
        row1 = self.get_row(row1)
        row2 = self.get_row(row2)
        result = []
        for i in row1:
            result[i] = row1[i] + row2[i]
        return result

    def sum_of_cols(self, col1: str, col2: str):
        col1 = self.get_col(col1)
        col2 = self.get_col(col2)
        result = []
        for i in col1:
            result[i] = col1[i] + col2[i]
        return result


# ------------------------ #
#       ERROR CLASS        #
# ------------------------ #
class Error:
    @staticmethod
    def raise_error(massage):
        print(f"ERROR: {massage}")
        return "ERROR"

    @staticmethod
    def raise_warning(massage):
        print(f"ERROR: {massage}")
        return "ERROR"


class XLsFile:

    def __init__(self, file: str, matrix_coords: dict, sheet_index=0):
        self.file = file
        self.name = file.split("/")[-1].split(".")[0]  # C:/folder1/folder2/file_path.extension >>> returns 'file_path'
        self.coordinates = matrix_coords
        self.sheet_index = sheet_index

        self.first_row, self.last_row = matrix_coords["first_row"], matrix_coords["last_row"]
        self.first_col, self.last_col = matrix_coords["first_col"], matrix_coords["last_col"]
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
        logger.info(" --- XlsFile.parse() ---")
        workbook = xlrd.open_workbook(self.file, encoding_override=ENCODING, on_demand=True)
        worksheet = workbook.sheet_by_index(self.sheet_index)

        rows = self._parse_rows(worksheet)
        if rows == "ERROR":
            self.dump_workbook(workbook)
            return "ERROR"

        cols = self._parse_cols(worksheet)
        if cols == "ERROR":
            self.dump_workbook(workbook)
            return "ERROR"

        self.dump_workbook(workbook)
        logger.info(f" Parsed, returning Matrix(): '{self.name}'", )
        return Matrix(name=self.name, rows=rows, cols=cols)

    def _parse_rows(self, worksheet):
        """The names of the rows are read vertically. The values of rows are read horizontally.
        So the first iteration is vertical and the second iteration is horizontal.
        :returns dictionary{'row': [val1, val2, ...]}"""
        logger.info(f" Parsing rows...")
        first_row, last_row = self.first_row, self.last_row
        first_col, last_col = self.first_col, self.last_col

        rows = {}
        empty_row_index = 1

        # Vertical Iteration / get rows's name
        the_column_which_has_all_rows_names = self.first_col - 1            # This is the cols that has rows' names
        for each_row in range(first_row, last_row + 1):                     # Added 1 otherwise it isn't inclusive
            row_name = self._pop_row_name(worksheet, rowx=each_row, start_colx=the_column_which_has_all_rows_names)
            row_vals = []    # reset the values for each rows

            if row_name != "":
                # Horizontal Iteration / get rows's values
                for each_col in range(first_col, last_col + 1):
                    value_of_each_column = self._pop_col_val(worksheet, colx=each_col, start_rowx=each_row)
                    # check value
                    if value_of_each_column == "ERROR":
                        error_massage = f"Cell has invalid value. Make sure all cell have ...!"
                        return Error.raise_error(error_massage)

                    row_vals.append(value_of_each_column)
                rows[row_name] = row_vals
                empty_row_index += 1
            else:
                logger.critical(f"{get_order(empty_row_index)} rows is empty!")

                error_massage = f"{get_order(empty_row_index)} rows is empty!" \
                                f"Make sure there are no gaps between rows."
                return Error.raise_error(error_massage)

        return rows

    def _parse_cols(self, worksheet):
        """The names of the cols are read horizontally. The values of cols are read vertically.
        The first iteration is horizontal. The second iteration is vertical.
        :returns dictionary{'col': [val1, val2, ...]}"""
        logger.info(f" Parsing cols...")
        first_row, last_row = self.first_row, self.last_row
        first_col, last_col = self.first_col, self.last_col

        cols = {}
        empty_col_index = 1  # tracking this for error

        the_row_which_has_all_cols_names = first_row - 1                    # This is the rows that has the cols' names

        # Horizontal Iteration / get cols's name
        for each_col in range(first_col, last_col + 1):                     # Added 1 otherwise it isn't inclusive
            col_name = self._pop_col_name(worksheet, colx=each_col, start_rowx=the_row_which_has_all_cols_names)
            col_vals = []   # reset the values for each cols

            if col_name != "":
                # Vertical Iteration / get cols's values
                for each_row in range(first_row, last_row + 1):
                    value_of_each_row = self._pop_row_val(worksheet, rowx=each_row, start_colx=each_col)
                    # check value
                    if value_of_each_row == "ERROR":
                        error_massage = "Invalid value in cell."
                        return Error.raise_error(error_massage)

                    col_vals.append(value_of_each_row)
                    empty_col_index += 1

                cols[col_name] = col_vals
            else:
                logger.critical(f"{get_order(empty_col_index)} column is empty!")

                error_massage = f"{get_order(empty_col_index)} column is empty! " \
                                f"Make sure there are no gaps between columns."
                return Error.raise_error(error_massage)

        return cols

    def _pop_row_name(self, worksheet, rowx, start_colx):
        row_vals = worksheet.row_values(rowx=rowx, start_colx=start_colx)  # list has only 1 item in it
        name = row_vals.pop(0)  # remove brackets from value
        if name in self.row_names:
            error_massage = f"Duplication detected in rows names: '{name}'." \
                            f"Make sure that all rows names are unique."
            return Error.raise_error(error_massage)
        else:
            self.row_names.append(name)
            return name

    def _pop_col_name(self, worksheet, colx, start_rowx):
        col_vals = worksheet.col_values(colx=colx, start_rowx=start_rowx)  # list has only 1 item in it
        name = col_vals.pop(0)  # remove brackets from value
        if name is self.row_names:
            error_massage = f"Duplication detected in column names: '{name}'." \
                            f"Make sure that all column names are unique."
            return Error.raise_error(error_massage)
        else:
            self.col_names.append(name)
            return name

    @staticmethod
    def _pop_row_val(worksheet, rowx, start_colx):
        row_vals = worksheet.row_values(rowx=rowx, start_colx=start_colx)  # list has only 1 item in it
        value = row_vals.pop(0)  # remove brackets from value
        # type check
        if type(value) == int or float or None:
            return value
        else:
            error_massage = f"Cell ({rowx}, {start_colx}) is not a number value." \
                            f"Make sure that all cells contain a number value."
            return Error.raise_error(error_massage)

    @staticmethod
    def _pop_col_val(worksheet, colx, start_rowx):
        col_vals = worksheet.col_values(colx=colx, start_rowx=start_rowx)  # list has only 1 item in it
        value = col_vals.pop(0)  # remove brackets from value
        if type(value) == int or float or None:
            return value
        else:
            error_massage = f"Cell ({start_rowx}, {colx}) is not a number value. " \
                            f"Make sure that all cells contain a number value."
            return Error.raise_error(error_massage)

    @staticmethod
    def dump_workbook(workbook):
        workbook.release_resources()
        del workbook


class Groups:
    """Groups is an abstraction of Matrix() object. It holds:
    - user_rows , user_cols : from user_matrix()
    - source_rows, source_cols: from source_matrix()
    - source_rows = ["John", "Jack", Daniel", "Jane", "Jennifer", "Samantha"]
    - user_row_group1 = {"Men": ["John", "Jack", Daniel"], "Women": ["Jane", "Jennifer", "Samantha"]}
    With Groups user is just managing lists, not actual rows and cols. After user is done
    with grouping rows and cols, this class will call a method that takes user's Groups()
    and returns a Matrix() object."""

    def __init__(self, source_matrix: Matrix):
        self.source_rows: list = source_matrix.get_rows()
        self.source_cols: list = source_matrix.get_cols()
        self.user_row_groups: dict = {}
        self.user_col_groups: dict = {}

    # ----------------- #
    #    GET METHODS    #
    # ----------------- #
    def get_user_row_groups(self):
        return self.user_row_groups

    def get_user_col_groups(self):
        return self.user_col_groups

    # ------------------------ #
    #    ADD/REMOVE METHODS    #
    # ------------------------ #
    def add_row_to_group(self, row: str, group: str):
        self.user_row_groups[group].append(row)
        self.source_rows.remove(row)

    def add_col_to_group(self, col: str, group: str):
        self.user_row_groups[group].append(col)
        self.source_cols.remove(col)

    def remove_row_from_group(self, row: str, group: str):
        self.user_col_groups[group].remove(row)
        self.source_rows.append(row)

    def remove_col_from_group(self, col: str, group: str):
        self.user_col_groups[group].remove(col)
        self.source_cols.append(col)

    # ------------------------ #
    #    CREATE/DEL METHODS    #
    # ------------------------ #

    def create_row_group(self, name):
        if name in self.user_row_groups.keys():
            error_massage = "Cannot create duplicate names."
            return Error.raise_error(error_massage)
        else:
            self.user_row_groups[name] = []
            return 1

    def create_col_group(self, name):
        if name in self.user_col_groups.keys():
            error_message = "Cannot create duplicate names."
            return Error.raise_error(error_message)
        else:
            self.user_col_groups[name] = []
            return 1

    def del_row_group(self, name):
        del self.user_row_groups[name]

    def del_col_group(self, name):
        del self.user_col_groups[name]

    @staticmethod
    def creates_duplication(group: list, element):
        """example_dict: {"group_name": ["e1", "e2", "e3"], "group_name2": ["e4", "e5", "e6"]}
        :param group :example_dict["group_name"] -> list to be searched
        :param element : str element"""
        e_count = 0
        # count element recursion
        for i in group:
            if group[i] == element:
                e_count += 1
        # if e_count is more than 1, that means there's a duplication
        if e_count > 1:
            return True
        else:
            return False


# ---------------- #
#    TEST CASES    #
# ---------------- #
file_correct = '../input_files/test_cases/xls_5-5.xls'
file_empty_row = '../input_files/test_cases/xls_5-5_empty_row.xls'
file_empty_col = '../input_files/test_cases/xls_5-5_empty_col.xls'

file_empty_cell = '../input_files/test_cases/xls_5-5_empty_cell.xls'
file_nan_cell = '../input_files/test_cases/xls_5-5_nan_cell.xls'
file_row_name_duplication = '../input_files/test_cases/xls_5-5_row_name_duplication.xls'
file_col_name_duplication = '../input_files/test_cases/xls_5-5_col_name_duplication.xls'

coords_correct = matrix_coordinates(rows=(2, 6), cols=("B", "F"))
coords_empty_row = matrix_coordinates(rows=(2, 7), cols=("C", "F"))
coords_empty_col = matrix_coordinates(rows=(2, 6), cols=("B", "G"))

coords_empty_cell = matrix_coordinates(rows=(2, 6), cols=("B", "F"))
coords_nan_cell = matrix_coordinates(rows=(2, 6), cols=("B", "F"))
coords_row_name_duplication = matrix_coordinates(rows=(2, 6), cols=("B", "F"))
coords_col_name_duplication = matrix_coordinates(rows=(2, 6), cols=("B", "F"))


xls_correct = XLsFile(file_correct, coords_correct)
xls_empty_row = XLsFile(file_empty_row, coords_empty_row)
xls_empty_col = XLsFile(file_empty_col, coords_empty_col)

xls_empty_cell = XLsFile(file_empty_cell, coords_empty_cell)
xls_nan_cell = XLsFile(file_nan_cell, coords_nan_cell)
xls_row_name_duplication = XLsFile(file_row_name_duplication, coords_row_name_duplication)
xls_col_name_duplication = XLsFile(file_col_name_duplication, coords_col_name_duplication)

logger.info(f" --- MATRIX CORRECT ---")
matrix_correct = xls_correct.parse()
if matrix_correct == "ERROR":
    print("error detected at my_matrix_correct")
else:
    matrix_correct.get_rows()
    matrix_correct.get_cols()
    matrix_correct.get_cell("derya", "muz")
    matrix_correct.get_row('ali')
    matrix_correct.get_row("esma")
    matrix_correct.get_col("ıspanak")
    matrix_correct.get_col('armut')

logger.info(" --- MATRIX EMPTY ROW ---")
matrix_empty_row = xls_empty_row.parse()
if matrix_empty_row == "ERROR":
    print(f"error detected at matrix_empty_row")
else:
    matrix_empty_row.get_rows()
    matrix_empty_row.get_cols()
    matrix_empty_row.get_cell("derya", "muz")
    matrix_empty_row.get_row('ali')
    matrix_empty_row.get_row("esma")
    matrix_empty_row.get_col("ıspanak")
    matrix_empty_row.get_col('armut')

logger.info(" --- MATRIX EMPTY COL ---")
matrix_empty_col = xls_empty_col.parse()
if matrix_empty_col == "ERROR":
    print("error detected at matrix_empty_col")
else:
    matrix_empty_col.get_rows()
    matrix_empty_col.get_cols()
    matrix_empty_col.get_cell("derya", "muz")
    matrix_empty_col.get_row('ali')
    matrix_empty_col.get_row("esma")
    matrix_empty_col.get_col("ıspanak")
    matrix_empty_col.get_col('armut')

logger.info(" --- MATRIX EMPTY CELL ---")
matrix_empty_cell = xls_empty_cell.parse()
if matrix_empty_cell == "ERROR":
    print(f"error detected at matrix_empty_cell")
else:
    matrix_empty_cell.get_rows()
    matrix_empty_cell.get_cols()
    matrix_empty_cell.get_cell("derya", "muz")
    matrix_empty_cell.get_row('ali')
    matrix_empty_cell.get_row("esma")
    matrix_empty_cell.get_col("ıspanak")
    matrix_empty_cell.get_col('armut')

# logger.info(" --- MATRIX NaN CELL ---")
# matrix_nan_cell = xls_nan_cell.parse()
# if matrix_nan_cell == "ERROR":
#     print(f"error detected on matrix_nan_cell")
# else:
#     matrix_nan_cell.get_rows()
#     matrix_nan_cell.get_cols()
#     matrix_nan_cell.get_cell("derya", "muz")
#     matrix_nan_cell.get_row('ali')
#     matrix_nan_cell.get_row("esma")
#     matrix_nan_cell.get_col("ıspanak")
#     matrix_nan_cell.get_col('armut')

# logger.info(" --- MATRIX ROW NAME DUPLICATION ---")
# matrix_row_name_duplication = xls_row_name_duplication.parse()
# if matrix_row_name_duplication == "ERROR":
#     print(f"error detected on matrix_empty_cell")
# else:
#     matrix_row_name_duplication.get_rows()
#     matrix_row_name_duplication.get_cols()
#     matrix_row_name_duplication.get_cell("derya", "muz")
#     matrix_row_name_duplication.get_row('ali')
#     matrix_row_name_duplication.get_row("esma")
#     matrix_row_name_duplication.get_col("ıspanak")
#     matrix_row_name_duplication.get_col('armut')
# matrix_col_name_duplication = xls_col_name_duplication.parse()