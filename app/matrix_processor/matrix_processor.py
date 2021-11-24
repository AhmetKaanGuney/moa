import os
from sqlite3.dbapi2 import OperationalError
import json
import sqlite3

from .converters import XlsFile, json_to_matrix, matrix_to_json
from .matrix import coordinates
from .errors import Error

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
CWD = os.getcwd()

database = f"{CWD}/db/matricies.db"
fallback_database = "./db/matricies.db"


# --------------------------- #
#     FILE TO BLUEPRINT       #
# --------------------------- #
def get_blueprint_from_file(file_stream, matrix_coordinates, session_id):
    # check file type
    # convert file to Matrix() object
    source_matrix = XlsFile(matrix_coordinates, file_stream=file_stream).parse()
    if source_matrix == None:
        return None

    # convert Matrix() object to json format
    matrix_for_db = matrix_to_json(source_matrix)

    try:
        conn = sqlite3.connect(database)
    except OperationalError:
        conn = sqlite3.connect(fallback_database)

    cur = conn.cursor()

    # store Matrix() in db with an id specific to session
    cur.execute(
        "REPLACE INTO matricies(session_id, matrix) VALUES(?, ?)",
        (session_id, matrix_for_db),
    )

    conn.commit()
    cur.close()
    conn.close()

    row_names = [k for k in source_matrix.rows]
    col_names = [k for k in source_matrix.cols]
    matrix_for_json = {
        "source": {"rows": row_names, "cols": col_names},
        "user": {"rowGroups": [], "colGroups": []},
    }
    blueprint = json.dumps(matrix_for_json, indent=4)
    return blueprint


# --------------------------- #
#     BLUEPRINT TO FILE       #
# --------------------------- #
def write_blueprint_to_file(blueprint, file_format, session_id, file_path):
    # Get matrix from db
    user_matrix = get_user_matrix_from_db(session_id)
    # Process matrix
    processed_matrix = blueprint_to_matrix(blueprint, user_matrix)
    # Write to file
    print(f"write_matrix_to_file() -> format = {file_format}")

    write_matrix_to_file(processed_matrix, file_format, file_path)


def get_user_matrix_from_db(session_id):
    try:
        conn = sqlite3.connect(database)
    except OperationalError:
        conn = sqlite3.connect(fallback_database)

    cur = conn.cursor()
    # Get user matrix
    cur.execute("SELECT matrix FROM matricies WHERE session_id=?", (session_id,))
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


def write_matrix_to_file(processed_matrix, target_format, file_path):
    if target_format == "xls":
        XlsFile.write(file_path, processed_matrix)
    else:
        print(f"WARNING!!!:\n\tFile Format: {target_format} not supported yet.")


if __name__ == "__main__":
    # get source file and matrix coordinates from client
    source_file = f"{CWD}/matrix_processor/test/input_files/5-5.xls"
    coordinates = coordinates((2, 6), ("b", "f"))

    session_id = 0

    print("--- matrix_processor.py ---")
    print("--- test mode ---")
    print("file_to_blueprint()")
    new_blueprint = get_blueprint_from_file(source_file, coordinates, session_id)
    print("blueprint_to_file()")
    write_blueprint_to_file(new_blueprint, "xls", session_id)
