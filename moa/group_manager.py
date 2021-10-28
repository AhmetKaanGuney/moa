from matrix import Matrix
from notification import Notification
import json


class GroupManager:
    """GroupManager is an abstraction of the Matrix() object. GroupManager makes it easy to reorganize the Matrix() object.
    When converting the groupings back to a Matrix() object,
    this class will sum the values of the grouped rows and columns.
    It holds:
        - user_rows , user_cols : from user_matrix()
        - source_rows, source_cols: from source_matrix()
        - source_rows = ["John", "Jack", Daniel", "Jane", "Jennifer", "Samantha"]
        - user_row_group1 = {"Men": ["John", "Jack", Daniel"], "Women": ["Jane", "Jennifer", "Samantha"]}
    With GroupManager the user is just managing lists of rows and cols names, not actual rows and cols. After user is done
    with grouping rows and cols, call a method that takes user's Groups() object
    and returns a Matrix() object."""

    def __init__(self, source_matrix: Matrix):
        self.source_matrix: Matrix = source_matrix
        self.source_rows: list = source_matrix.get_rows()
        self.source_cols: list = source_matrix.get_cols()
        self.user_row_groups: dict = {}
        self.user_col_groups: dict = {}
        
    # ----------------- #
    #    GET METHODS    #
    # ----------------- #
    def get_row_groups(self) -> dict:
        """retruns: all the row group names"""
        return self.user_row_groups

    def get_col_groups(self) -> dict:
        """retruns: all the col group names"""
        return self.user_col_groups

    def get_row_group(self, group: str) -> list:
        """returns: value of row group as list"""
        return self.user_row_groups[group]

    def get_col_group(self, group: str) -> list:
        """returns: value of col group as list"""
        return self.user_col_groups[group]

    # ------------------------ #
    #    ADD/REMOVE METHODS    #
    # ------------------------ #
    def add_rows_to_group(self, rows: list, group: str):
        """ 1. adds rows to the group
        2. then removes the added rows from source rows
        A row can only exist in one place."""
        for r in rows:
            self.user_row_groups[group].append(r)
            self.source_rows.remove(r)

    def add_cols_to_group(self, cols: list, group: str):
        """ 1. adds cols to the group
        2. then removes the added cols from source rows
        A col can only exist in one place."""
        for c in cols:
            self.user_col_groups[group].append(c)
            self.source_cols.remove(c)

    def remove_rows_from_group(self, rows: str, group: str):
        """- remove rows from the group
        - then adds the removed rows back to source rows
        A row can only exist in one place."""
        for r in rows:
            self.user_row_groups[group].remove(r)
            self.source_rows.append(r)

    def remove_cols_from_group(self, cols: str, group: str):
        """- remove cols from the group
        -  then adds the removed cols back to source cols
        A col can only exist in one place."""
        for c in cols:
            self.user_col_groups[group].remove(c)
            self.source_cols.append(c)

    # ------------------------ #
    #    CREATE/DEL METHODS    #
    # ------------------------ #

    def create_row_group(self, name):
        """Creates a new key in the user_row_group. Raises error if name already exists."""
        if name in self.user_row_groups.keys():
            return Notification.raise_error(message="Cannot create duplicate rows names.")
        else:
            self.user_row_groups[name] = []
            return self.user_row_groups

    def create_col_group(self, name):
        """Creates a new key in the user_col_group. Raises error if name already exists."""
        if name in self.user_col_groups.keys():
            return Notification.raise_error(message="Cannot create duplicate column names.")
        else:
            self.user_col_groups[name] = []
            return self.user_col_groups

    def del_row_group(self, name):
        """1. copies row names inside the row group back to source rows.
        2. then deletes the group.
        3. returns: user_row_groups: (dict)
        Raises error if given name isn't in the user_row_groups"""
        if name in self.user_row_groups.keys():
            # Copy rows back to source rows
            for i in self.user_row_groups[name]:
                self.source_rows.append(i)

            del self.user_row_groups[name]
            return self.user_row_groups
        else:
            return Notification.raise_error(message=f" >>> Cannot Delete Row : '{name}' doesn't exist.")

    def del_col_group(self, name):
        """1. copies col names inside the col group back to source cols.
        2. then deletes the group.
        3. returns: user_col_groups: (dict)
        Raises error if given name isn't in the user_col_groups"""
        if name in self.user_col_groups.keys():
            # Copy cols back to source cols
            for i in self.user_col_groups[name]:
                self.source_cols.append(i)

            del self.user_col_groups[name]
            return self.user_col_groups
        else:
            return Notification.raise_error(message=f" >>> Cannot Delete Col : '{name}' doesn't exist.")

    # -------------------- #
    #    RENAME METHODS    #
    # -------------------- #
    def rename_row_group(self, new_name, group_name):
        """Copies the values of the group to a new group with the same name.
         Then deletes the group with the old name"""
        self.user_row_groups[new_name] = self.user_row_groups[group_name]
        del self.user_row_groups[group_name]

    def rename_col_group(self, new_name, group_name):
        """Copies the values of the group to a new group with the new_name.
         Then deletes the group with the old name"""
        self.user_col_groups[new_name] = self.user_col_groups[group_name]
        del self.user_col_groups[group_name]

    # ----------------------- #
    #    CONVERT TO MATRIX    #
    # ----------------------- #
    def convert_to_matrix(self):
        """- returns: Matrix()"""
        output_matrix = self._sum_groups()
        return output_matrix

    def _sum_groups(self):
        """Each child method in this function takes a matrix then returns a new matrix with summed values.
        The returning matricies' have updated row or col depending on the method.
        If _sum_row_groups() is called then it returns a Matrix() object with summed rows and 'updated' cols.
        What 'updated' means is that if it didn't got updated the corresponding values of the rows and cols would be
        out of sync. For example: The rows gets summed, but the values inside the columns wouldn't change.
        The cols would hold the old values of the rows. So rows and cols would clash with each other."""
        matrix_name = self.source_matrix.get_name()
        rows_summed_matrix = self._sum_row_groups(self.source_matrix)
        row_and_cols_summed_matrix = self._sum_col_groups(rows_summed_matrix)
        return row_and_cols_summed_matrix

    def _sum_row_groups(self, matrix: Matrix):
        """Sums the rows and updates the cols values.
        returns: Matrix(summed_rows, updated_cols)"""
        matrix_name = matrix.get_name()
        row_groups = self.user_row_groups
        summed_rows = {}
        updated_cols = {}

        # Sum Rows
        for group in row_groups:
            rows_to_be_summed = row_groups[group]

            if len(rows_to_be_summed) < 1:
                Notification.raise_warning(f" WARNING! Empty row group detected: '{group}'.")
                return "ERROR"
            else:
                summed_rows[group] = matrix.sum_rows(rows_to_be_summed)

        # Update Cols
        c_length = len(matrix.get_cols())
        # Horizontal Iteration
        for c in range(c_length):
            cols_to_be_summed = matrix.get_cols()
            c_name = cols_to_be_summed[c]

            updated_cols[c_name] = []
            # Vertical Iteration
            for r in summed_rows:
                cell_val = summed_rows[r][c]
                updated_cols[c_name].append(cell_val)

        rows_summed_matrix = Matrix(matrix_name, summed_rows, updated_cols)
        return rows_summed_matrix

    def _sum_col_groups(self, matrix: Matrix):
        """Sums the cols and updates the rows values.
        returns: Matrix(updated_rows, summed_cols)"""
        matrix_name = matrix.get_name()
        col_groups = self.user_col_groups
        summed_cols = {}
        updated_rows = {}

        # Sum Cols
        for group in col_groups:
            cols_to_be_summed = col_groups[group]

            if len(cols_to_be_summed) < 1:
                Notification.raise_warning(f" WARNING! Empty row group detected: '{group}'.")
                return "ERROR"
            else:
                summed_cols[group] = matrix.sum_cols(cols_to_be_summed)

        # Update Rows
        rows = matrix.get_rows()
        cols = [k for k in summed_cols]
        r_length = len(rows)
        c_length = len(cols)

        for r in range(r_length):
            row_name = rows[r]
            updated_rows[row_name] = []

            for c in range(c_length):
                col_name = cols[c]
                cell_val = summed_cols[col_name][r]
                updated_rows[row_name].append(cell_val)

        cols_summed_matrix = Matrix(matrix_name, updated_rows, summed_cols)
        return cols_summed_matrix
    
    # ------------------------------ #
    #    CONSTRUCT WITH BLUEPRINT    #
    # ------------------------------ #
    def build_with(self, blueprint):
        self.user_row_groups = blueprint["rows"]
        self.user_col_groups = blueprint["cols"]
        
        return self.convert_to_matrix()
