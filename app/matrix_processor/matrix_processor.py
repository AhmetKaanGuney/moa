import os
from sqlite3.dbapi2 import OperationalError
import json
import sqlite3

from converters import XlsFile, json_to_matrix
from matrix import matrix_coordinates
from group_manager import GroupManager

cwd = os.getcwd()
print("cwd: ", cwd)

# How this program works :
# There are 2 stages:
# 1. File to Blueprint
# 2. Blueprint to File

# 1. File to Blueprint:
#   user sends file to server
#   server reads it and returns a blueprint
#   blueprint contains:
#       - names of each row and col in the source matrix
#         in the form of
#       - source_rows, source_cols
#
# 2. Blueprint to File:
#   user submits the blueprint
#   blueprint contains:
#       - user_row_groups,
#       - user_col_groups,
#       - export_format
#
#   server processes source file's matrix data according to
#   users groupings on the blueprint
#
#   server returns a file containing the new matrix, in a
#   format that user has specified

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# !!! ALWAYS HANDLE JSON AS UTF-8 !!! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

database = f"{cwd}/../db/matricies.db"
fallback_database = "./moa/db/matricies.db"

# get source file and matrix coordinates from client
coordinates = matrix_coordinates((2, 6), ("b", "f"))
source_file = f"{cwd}/../test/input_files/5-5.xls"

user_id = 0
request = "blueprint_to_file"


# Entry Point
def main(request: str, user_id: int):
    """Handles request for specific user"""

    if request == "file_to_blueprint":
        blueprint = file_to_blueprint(source_file, coordinates, user_id)
        # return blueprint json to client
        print("TODO -> return blueprint to client")
        print(blueprint)

    if request == "blueprint_to_file":
        with open(f"{cwd}/../test/input_files/blueprint.json", encoding="utf-8") as f:
            blueprint = json.load(f)
        target_format = "xls"
        user_matrix = get_user_matrix_from_db(user_id)
        processed_matrix = blueprint_to_matrix(blueprint, user_matrix)
        f = convert_matrix_to_target_format(processed_matrix, target_format)
        print("TODO -> send file to client")


# --------------------------- #
#     FILE TO BLUEPRINT       #
# --------------------------- #
def file_to_blueprint(source_file, coordinates, user_id):
    # check file type
    # convert file to Matrix() object
    source_matrix = XlsFile(source_file, coordinates).parse()

    # convert Matrix() object to json format
    rows = source_matrix.rows
    cols = source_matrix.cols
    matrix = {"rows": rows, "cols": cols}
    blueprint = json.dumps(matrix, indent=4)

    # store Matrix() in db with an id specific to user
    try:
        conn = sqlite3.connect(database)
    except OperationalError:
        conn = sqlite3.connect(fallback_database)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO matricies (user_id, matrix) VALUES (?, ?)",
        (user_id, blueprint),
    )
    conn.commit()
    cur.close()
    conn.close()

    return blueprint


# --------------------------- #
#     BLUEPRINT TO FILE       #
# --------------------------- #
def get_user_matrix_from_db(user_id):
    try:
        conn = sqlite3.connect(database)
    except OperationalError:
        conn = sqlite3.connect(fallback_database)

    cur = conn.cursor()
    cur.execute("SELECT matrix FROM matricies WHERE user_id=?", (user_id,))
    user_matrix = cur.fetchone()[0]
    cur.close()
    conn.close()
    return user_matrix


def blueprint_to_matrix(blueprint: str, matrix: str):
    # convert json to matrix object
    source_matrix = json_to_matrix(matrix)

    # initialize GroupManager with source matrix
    gm = GroupManager(source_matrix)

    # create groups according to blueprint
    processed_matrix = gm.build_with(blueprint)
    return processed_matrix


def convert_matrix_to_target_format(processed_matrix, target_format):
    if target_format == "xls":
        print("TODO -> convert_matrix_to_target_format()")
        print("processed_matrix:")
        print(processed_matrix.rows)
        print(processed_matrix.cols)


if __name__ == "__main__":
    main(request, user_id)
