# -----------------------  #
#         MATRIX           #
# -----------------------  #
from xlrd.formula import rownamerel


class Matrix:
    """This class is for holding raw matrix data in the form of two dictionaries. One for row and one for columns.\n
    Every Matrix() object has these attributes:
        - name : name of the Matrix() object
        - rows : a dict that has rows names as keys and lists as their values
        - cols : a dict that has cols name as keys and lists as their values
        - example row: {'row1': [val1, val2, val3], 'row2': [val4, val5], ...}"""

    def __init__(self, rows: dict, cols: dict):
        self.rows = rows
        self.cols = cols

    def __repr__(self) -> str:
        row_str = "Rows: {\n\t"
        for r in self.get_rows():
            row_str += f"'{r:<15}':["
            for i in self.get_row(r):
                row_str += f"{i},"
            row_str += "]\n\t"
        row_str += "},"

        col_str = "Cols: {\n\t"
        for c in self.get_cols():
            col_str += f"'{c:<15}':["
            for i in self.get_col(c):
                col_str += f"{i},"
            col_str += "]\n\t"
        col_str += "}"
        return row_str + "\n" + col_str
    # ----------------- #
    #    GET METHODS    #
    # ----------------- #
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
        # some functions side effect is modifying the matrix's rows and cols
        # it's happening outside of the object i suppose
        # probably in sum rows and cols in the group manager look at there
        # make sure that is doesnt alter source rows and cols
        # just copies the data and summs that data
        col_len = 0
        try:
            col_len = len(self.get_col(cols[0]))
        except KeyError:
            print(f"The item: '{cols[0]}', not in self.cols \n{self.cols}")
            raise KeyError
        result_col = [0*i for i in range(0, col_len)]

        for name in cols:
            for i in range(0, col_len):
                col = self.get_col(name)
                result_col[i] += col[i]
        return result_col


# ------------------------ #
#       Coordinates        #
# ------------------------ #
def coordinates(rows: tuple, cols: tuple):
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


if __name__ == "__main__":
    m_name = "test"
    m_rows = {}
    m_cols = {}
    for i in range(0, 5):
        row = chr(65 + i)
        m_rows[row] = [i + 1, i + 2, i + 3]

    for i in range(0, 5):
        col = chr(65 + i)
        m_cols[col] = [i + 1, i + 2, i + 3]

    matrix_test = Matrix(m_name, m_rows, m_cols)

    print("Get rows: ", matrix_test.get_rows())
    for i in range(0, 5):
        print(f"{chr(65 + i)} :", matrix_test.get_row(chr(65+i)))
    print("---")
    print("Get cols: ", matrix_test.get_cols())
    for i in range(0, 5):
        print(f"{chr(65 + i)} :", matrix_test.get_col(chr(65+i)))
    print("---")

    print(matrix_test.sum_rows(["A", "E"]))
    print(matrix_test.sum_cols(["A", "E"]))

