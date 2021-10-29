<<<<<<< HEAD
from matrix import Matrix
from group_manager import GroupManager
from converters import XlsFile
import logging
import os
import sys

# Go to upper directory and then import files
cwd = os.getcwd()
parentdir = os.path.dirname(cwd)
sys.path.append(parentdir)
print("parent dir: ", parentdir)
=======
import logging
import os, sys

cwd = os.getcwd()
parentdir = os.path.dirname(cwd)
sys.path.append(parentdir)
print(parentdir )

from group_manager import GroupManager
from matrix import Matrix
from converters import XlsFile
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b


ENCODING = "UTF-8"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(message)s")

parentdir = os.path.dirname(parentdir)
sys.path.append(parentdir)

<<<<<<< HEAD
file_handler = logging.FileHandler(
    parentdir + "/moa/logs/engine_test.log", mode="a", encoding=ENCODING)
=======
file_handler = logging.FileHandler("/VsCodeProjects/moa/logs/engine_test.log", mode="a", encoding=ENCODING)
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def clear_log():
    try:
<<<<<<< HEAD
        my_log = open(parentdir + "/moa/logs/engine_test.log", "w")
=======
        my_log = open("/VsCodeProjects/moa/logs/engine_test.log", "w")
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
        my_log.write("")
        my_log.close()
    except FileNotFoundError:
        pass


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

<<<<<<< HEAD
    coord = {"first_row": f_row, "last_row": l_row,
             "first_col": f_col, "last_col": l_col}
=======
    coord = {"first_row": f_row, "last_row": l_row, "first_col": f_col, "last_col": l_col}
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
    logger.debug(f" Returning coordinates. \n"
                 f"\t- first_row : {coord['first_row']}\n"
                 f"\t- last_row : {coord['last_row']}\n"
                 f"\t- first_col : {coord['first_col']}\n"
                 f"\t- last_col : {coord['last_col']}")
    return coord


# ---------------------------- #
#       Matrix Functions       #
# ---------------------------- #
def run_matrix_methods(matrix):
    logger.info(f" Matrix : {matrix.name}")
    row_names = matrix.get_rows()
    col_names = matrix.get_cols()
    logger.info(f" Get Rows :\t{matrix.get_rows()}")
    logger.info(f" Get Cols :\t{matrix.get_cols()}")
    for i in range(0, 3):
        row = row_names[i]
        col = col_names[i]
        logger.info(f" Get Row : '{row}' :\t{matrix.get_row(row)}")
        logger.info(f" Get Col : '{col}' :\t{matrix.get_col(col)}")
<<<<<<< HEAD
        logger.info(
            f" Get Cell : ({row},{col}) :\t{matrix.get_cell(row, col)}")
=======
        logger.info(f" Get Cell : ({row},{col}) :\t{matrix.get_cell(row, col)}")
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b


# ---------------------------- #
#       Groups Functions       #
# ---------------------------- #
def run_groups_methods(groups):
    source_row_names = [i for i in groups.source_rows]
    source_col_names = [i for i in groups.source_cols]
    # ----------------------- #
    #     CREATE METHODS      #
    # ----------------------- #
    # Create Row Group
    logger.info(" CREATE METHODS")
    logger.info(f" User Row Groups : {groups.get_row_groups()}")
    for i in range(0, 3):
        group_name = chr(90 - i)
        logger.info(f" >>> Creating Row Group : {group_name}")
        groups.create_row_group(group_name)
    logger.info(f" User Row Groups : {groups.get_row_groups()}")

    # Create Col Group
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    for i in range(0, 3):
        group_name = chr(90 - i)
        logger.info(f" >>> Creating Col Group : {group_name}")
        groups.create_col_group(group_name)
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info("")

    # ----------------------- #
    #     RENAME METHODS      #
    # ----------------------- #
    logger.info(" >>>")
    logger.info(" RENAME METHODS")

    # Rename Rows
    logger.info(f" User Row Groups : {groups.get_row_groups()}")
    for i in range(0, 3):
        group_name = chr(90 - i)
        new_name = chr(65 + i)
<<<<<<< HEAD
        logger.info(
            f" >>> Renaming Row Group : {group_name} --> to {new_name}")
=======
        logger.info(f" >>> Renaming Row Group : {group_name} --> to {new_name}")
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
        groups.rename_row_group(new_name=new_name, group_name=group_name)
    logger.info(f" User Row Groups : {groups.get_row_groups()}")

    # Rename Cols
    logger.info(" >>>")
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    for i in range(0, 3):
        group_name = chr(90 - i)
        new_name = chr(65 + i)
<<<<<<< HEAD
        logger.info(
            f" >>> Renaming Col Group : {group_name} --> to {new_name}")
=======
        logger.info(f" >>> Renaming Col Group : {group_name} --> to {new_name}")
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
        groups.rename_col_group(new_name=new_name, group_name=group_name)
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info("")

    # -------------------- #
    #     ADD METHODS      #
    # -------------------- #
    # Add Rows
    logger.info(" ADD METHODS")
    logger.info(f" User Row Groups : {groups.get_row_groups()}")
    for i in range(0, 3):
        group_name = chr(65 + i)
        rows = [source_row_names[i]]
        logger.info(f" >>> Add Row : '{rows}' --> to Group : '{group_name}'")
        groups.add_rows_to_group(rows=rows, group=group_name)
    # groups.add_rows_to_group(rows=["ibrahim"], group="A")
    logger.info(f" User Row Groups : {groups.get_row_groups()}")

    # Add Cols
    logger.info(" >>>")
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    for i in range(0, 3):
        group_name = chr(65 + i)
        cols = [source_col_names[i]]
        logger.info(f" >>> Add Col : '{cols}' --> to Group : '{group_name}'")
        groups.add_cols_to_group(cols=cols, group=group_name)
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info("")

    # ---------------------- #
    #     REMOVE METHODS     #
    # ---------------------- #
    # Remove Rows
    logger.info(" REMOVE METHODS ")
    logger.info(f" User Row Groups : {groups.get_row_groups()}")
    logger.info(f" Source Rows : {groups.source_rows}")
    for i in range(0, 3):
        group_name = chr(65 + i)
        rows = [source_row_names[i]]
<<<<<<< HEAD
        logger.info(
            f" >>> Remove Row : '{rows}' --> from Group : '{group_name}'")
=======
        logger.info(f" >>> Remove Row : '{rows}' --> from Group : '{group_name}'")
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
        groups.remove_rows_from_group(rows=rows, group=group_name)
    logger.info(f" User Row Groups : {groups.get_row_groups()}")
    logger.info(f" Source Rows : {groups.source_rows}")

    # Remove Cols
    logger.info(" >>>")
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info(f" Source Cols : {groups.source_cols}")
    for i in range(0, 3):
        group_name = chr(65 + i)
        cols = [source_col_names[i]]
<<<<<<< HEAD
        logger.info(
            f" >>> Remove Col : '{cols}' --> from Group : '{group_name}'")
=======
        logger.info(f" >>> Remove Col : '{cols}' --> from Group : '{group_name}'")
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
        groups.remove_cols_from_group(cols=cols, group=group_name)
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info(f" Source Cols : {groups.source_cols}")
    logger.info("")

    # ----------------------- #
    #     DELETE METHODS      #
    # ----------------------- #

    # Delete Row Group
    logger.info(" DELETE METHODS")
    logger.info(f" User Row Groups : {groups.get_row_groups()}")
    logger.info(f" Source Rows : {groups.source_rows}")
    for i in range(0, 3):
        group_name = chr(65 + i)
        logger.info(f" >>> Deleting Row Group : {group_name}")
        groups.del_row_group(group_name)
    logger.info(f" User Row Groups : {groups.get_row_groups()}")
    logger.info(f" Source Rows : {groups.source_rows}")

    # Delete Col Group
    logger.info(" >>>")
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info(f" Source Cols : {groups.source_cols}")
    for i in range(0, 3):
        group_name = chr(65 + i)
        logger.info(f" >>> Deleting Col Group : {group_name}")
        groups.del_col_group(group_name)
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info(f" Source Cols : {groups.source_cols}")
    logger.info("")

<<<<<<< HEAD

=======
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
def convert_groups_to_matrix(groups):
    source_row_names = [i for i in groups.source_rows]
    source_col_names = [i for i in groups.source_cols]

    logger.info(f" --- CONVERT GROUPS to MATRIX ---")
    # Create Row Group
    for i in range(0, 2):
        group_name = chr(65 + i)
        groups.create_row_group(group_name)
    logger.info(f" User Row Groups : {groups.get_row_groups()}")

    # Create Col Group
    for i in range(0, 2):
        group_name = chr(65 + i)
        groups.create_col_group(group_name)
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info("")

    # Add Rows
    for i in range(0, 2):
        group_name = chr(65 + i)
        rows = [source_row_names[i], source_row_names[i + 2]]
        groups.add_rows_to_group(rows=rows, group=group_name)
    logger.info(f" User Row Groups : {groups.get_row_groups()}")

    # Add Cols
    logger.info(" >>>")
    for i in range(0, 2):
        group_name = chr(65 + i)
        cols = [source_col_names[i], source_col_names[i + 2]]
        groups.add_cols_to_group(cols=cols, group=group_name)
    logger.info(f" User Col Groups : {groups.get_col_groups()}")
    logger.info("")
    # ----------------------- #
    #     CONVERT METHOD      #
    # ----------------------- #
    output_matrix: Matrix = groups.convert_to_matrix()
    if output_matrix == "ERROR":
        logger.info(" Error detected while converting.")
    else:
        logger.info(f" --- OUTPUT MATRIX ---")
        logger.info(f" Name : {output_matrix.name}")
        for i in range(0, 2):
            name = chr(65+i)
            logger.info(f" Row : {name}: {output_matrix.get_row(name)}")
            logger.info(f" Col : {name}: {output_matrix.get_col(name)}")
        return output_matrix
<<<<<<< HEAD


=======
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
# ---------------- #
#    TEST CASES    #
# ---------------- #
clear_log()

<<<<<<< HEAD
file_correct = parentdir + '/moa/test/input_files/5-5.xls'
file_empty_col = parentdir + '/moa/test/input_files/5-5_empty_col.xls'
file_empty_row = parentdir + '/moa/test/input_files/5-5_empty_row.xls'

file_empty_cell = parentdir + '/moa/test/input_files/5-5_empty_cell.xls'
file_nan_cell = parentdir + '/moa/test/input_files/5-5_nan_cell.xls'
file_row_name_duplication = parentdir + \
    '/moa/test/input_files/5-5_row_name_duplication.xls'
file_col_name_duplication = parentdir + \
    '/moa/test/input_files/5-5_col_name_duplication.xls'
=======
file_correct = 'D://VsCodeProjects/moa/src/test/input_files/5-5.xls'
file_empty_col = 'D://VsCodeProjects/moa/src/test/input_files/5-5_empty_col.xls'
file_empty_row = 'D://VsCodeProjects/moa/src/test/input_files/5-5_empty_row.xls'

file_empty_cell = 'D://VsCodeProjects/moa/src/test/input_files/5-5_empty_cell.xls'
file_nan_cell = 'D://VsCodeProjects/moa/src/test/input_files/5-5_nan_cell.xls'
file_row_name_duplication = 'D://VsCodeProjects/moa/src/test/input_files/5-5_row_name_duplication.xls'
file_col_name_duplication = 'D://VsCodeProjects/moa/src/test/input_files/5-5_col_name_duplication.xls'
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b

coords_correct = matrix_coordinates(rows=(2, 6), cols=("B", "F"))
coords_empty_row = matrix_coordinates(rows=(2, 7), cols=("C", "F"))
coords_empty_col = matrix_coordinates(rows=(2, 6), cols=("B", "G"))

coords_empty_cell = matrix_coordinates(rows=(2, 6), cols=("B", "F"))
coords_nan_cell = matrix_coordinates(rows=(2, 6), cols=("B", "F"))
coords_row_name_duplication = matrix_coordinates(rows=(2, 6), cols=("B", "F"))
coords_col_name_duplication = matrix_coordinates(rows=(2, 6), cols=("B", "F"))


xls_correct = XlsFile(file_correct, coords_correct)
xls_empty_row = XlsFile(file_empty_row, coords_empty_row)
xls_empty_col = XlsFile(file_empty_col, coords_empty_col)

xls_empty_cell = XlsFile(file_empty_cell, coords_empty_cell)
xls_nan_cell = XlsFile(file_nan_cell, coords_nan_cell)
<<<<<<< HEAD
xls_row_name_duplication = XlsFile(
    file_row_name_duplication, coords_row_name_duplication)
xls_col_name_duplication = XlsFile(
    file_col_name_duplication, coords_col_name_duplication)
=======
xls_row_name_duplication = XlsFile(file_row_name_duplication, coords_row_name_duplication)
xls_col_name_duplication = XlsFile(file_col_name_duplication, coords_col_name_duplication)
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
# ---------- #
#    PARSE   #
# ---------- #
logger.info(f" --- PARSE CORRECT ---")
matrix_correct = xls_correct.parse()
if matrix_correct == "ERROR":
    logger.info(f" Error detected while parsing.")

logger.info(f" --- PARSE EMPTY_ROW ---")
matrix_empty_row = xls_empty_row.parse()
if matrix_empty_row == "ERROR":
    logger.info(f" Error detected while parsing.")

logger.info(f" --- PARSE EMPTY_COL ---")
matrix_empty_col = xls_empty_col.parse()
if matrix_empty_col == "ERROR":
    logger.info(f" Error detected while parsing.")

logger.info(f" --- PARSE EMPTY_CELL---")
matrix_empty_cell = xls_empty_cell.parse()
if matrix_empty_cell == "ERROR":
    logger.info(f" Error detected while parsing.")

# ------------------------------ #
#       RUN MATRIX METHODS       #
# ------------------------------ #
if matrix_correct == "ERROR":
    pass
else:
    logger.info("")
    logger.info(f" --- MATRIX CORRECT ---")
    run_matrix_methods(matrix_correct)

if matrix_empty_row == "ERROR":
    pass
else:
    logger.info("")
    logger.info(" --- MATRIX EMPTY ROW ---")
    run_matrix_methods(matrix_empty_row)

if matrix_empty_col == "ERROR":
    pass
else:
    logger.info("")
    logger.info(" --- MATRIX EMPTY COL ---")
    run_matrix_methods(matrix_empty_col)

if matrix_empty_cell == "ERROR":
    pass
else:
    logger.info("")
    logger.info(" --- MATRIX EMPTY CELL ---")
    run_matrix_methods(matrix_empty_cell)

<<<<<<< HEAD

def write_matrix_to_xls_file(matrix: Matrix):
    file_name = "test.xls"
    folder_path = parentdir + "/moa/test/output_files/"
    os.remove(folder_path+file_name)
    file_path = file_name + folder_path
    XlsFile.write(file_path, matrix)


=======
def write_matrix_to_xls_file(matrix: Matrix):
    file_name = "test.xls"
    folder_path = "../output_files/"
    os.remove(folder_path+file_name)
    file_path = file_name + folder_path
    XlsFile.write(file_path, matrix)
>>>>>>> fc1f8d95e066af5673b3b21adc716838ba99110b
# ----------------------------- #
#       RUN GROUP METHODS       #
# ----------------------------- #
if matrix_correct == "ERROR":
    pass
else:
    logger.info("")
    logger.info(f" --- GROUPS CORRECT ---")
    groups_correct = GroupManager(matrix_correct)
    run_groups_methods(groups_correct)
    output_matrix = convert_groups_to_matrix(groups_correct)

    write_matrix_to_xls_file(output_matrix)
