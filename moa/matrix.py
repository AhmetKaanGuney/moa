# -----------------------  #
#         MATRIX           #
# -----------------------  #
class Matrix:
    """This class is for holding raw matrix data in the form of two dictionaries. One for row and one for columns.\n
    Every Matrix() object has these attributes:
        - name : name of the Matrix() object
        - rows : a dict that has rows names as keys and lists as their values
        - cols : a dict that has cols name as keys and lists as their values
        - example row: {'row1': [val1, val2, val3], 'row2': [val4, val5], ...}"""

    def __init__(self, rows: dict, cols: dict, name=None):
        self.name = name
        self.rows = rows
        self.cols = cols

    # ----------------- #
    #    GET METHODS    #
    # ----------------- #
    def get_name(self):
        """returns: self.name"""
        return self.name

    def get_rows(self):
        """returns: all of the rows' name in a list"""
        row_names = []
        for name in self.rows.keys():
            row_names.append(name)
        return row_names

    def get_cols(self):
        """returns: all of the cols' name in a list"""
        col_names = []
        for name in self.cols.keys():
            col_names.append(name)
        return col_names

    def get_cell(self, row: str, col: str):
        """returns: data at position (row, col)"""
        i = 0
        # Vertical iteration
        for c in self.cols:
            if c == col:
                break
            else:
                i += 1
        cell = self.rows[row][i]
        return cell

    def get_row(self, name: str):
        return self.rows[name]

    def get_col(self, name: str):
        return self.cols[name]

    # ------------------------ #
    #    ADD/REMOVE METHODS    #
    # ------------------------ #

    def sum_rows(self, rows: list):
        """sums the rows that are in the given list and returns the resulting row values in a list."""
        row_len = len(self.get_row(rows[0]))
        # populate the resulting row list with zeros
        result_row = [0*i for i in range(0, row_len)]

        for name in rows:
            for i in range(0, row_len):
                row = self.get_row(name)
                result_row[i] += row[i]
        return result_row

    def sum_cols(self, cols: list):
        """sums the cols that in the given list and returns the resulting col values in a list."""
        col_len = len(self.get_col(cols[0]))
        result_col = [0*i for i in range(0, col_len)]

        for name in cols:
            for i in range(0, col_len):
                col = self.get_col(name)
                result_col[i] += col[i]
        return result_col


# ------------------------ #
#       Coordinates        #
# ------------------------ #
def matrix_coordinates(rows: tuple, cols: tuple):
    """You can think of the Matrix as a rectangle. The parser needs to know all the four coordinates.\n
    Every value is subtracted by 1 so user can enter what is shown on the Excel groups. \n
    Then this function adjusts these values to be compatible with zero indexing and returns.
    :param rows (first_row, last_row) >> takes int
    :param cols (first_col, last_col) >> takes string
    :returns dictionary
    """
    f_row, l_row = rows[0] - 1, rows[1] - 1

    # col_tup[0] = 'A' >>> 'A' == 1 >>> returns 'A' - 1
    f_col, l_col = col_to_num(cols[0]) - 1, col_to_num(cols[1]) - 1

    coord = {"first_row": f_row, "last_row": l_row, "first_col": f_col, "last_col": l_col}
    return coord


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


# m_name = "test"
# m_rows = {}
# m_cols = {}
# for i in range(0, 5):
#     row = chr(65 + i)
#     m_rows[row] = [i + 1, i + 2, i + 3]
#
# for i in range(0, 5):
#     col = chr(65 + i)
#     m_cols[col] = [i + 1, i + 2, i + 3]
#
# matrix_test = Matrix(m_name, m_rows, m_cols)
#
# print("Get rows: ", matrix_test.get_rows())
# for i in range(0, 5):
#     print(f"{chr(65 + i)} :", matrix_test.get_row(chr(65+i)))
# print("---")
# print("Get cols: ", matrix_test.get_cols())
# for i in range(0, 5):
#     print(f"{chr(65 + i)} :", matrix_test.get_col(chr(65+i)))
# print("---")
#
# print(matrix_test.sum_rows(["A", "E"]))
# print(matrix_test.sum_cols(["A", "E"]))

