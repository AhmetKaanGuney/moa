#!../venv/Scripts/python.exe

import json
import logging
import sqlite3

import flask

from converters import XlsFile, json_to_matrix
from matrix import Matrix, col_to_num, matrix_coordinates
from group_manager import GroupManager

# ENCODING = "UTF-8"
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter("%(levelname)s:%(message)s")
# file_handler = logging.FileHandler("../logs/flask_test.log", mode="a", encoding=ENCODING)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# How this program works :
# user sends file to server
# server reads it and returns a blueprint which only contains source file's row and col names
# user groups these names
# user submits the blueprint
# server processes source file's matrix data according to users groupings on the blueprint
# server returns a file containing the new matrix, in a format that user has specified


# Entry Point
def main():
    # blueprint = matrix_to_blueprint(source_file, coordinates, user_id)
    # # return blueprint json to client
    # print("ADDED to db: ")
    # print(blueprint)
    pass

# There are 2 stages of interaction between server and client

# First is:
# --------------------------- #
#     MATRIX TO BLUEPRINT     #
# --------------------------- #
database = "../db/matricies.db"
# get source file and matrix coordinates from client
coordinates = matrix_coordinates((2, 6), ("b", "f"))
source_file = "../test/input_files/5-5.xls"
user_id = 3


def matrix_to_blueprint(source_file, coordinates, user_id):
    # check file type
    # convert file to Matrix() object
    source_matrix = XlsFile(source_file, coordinates).parse()

    # convert Matrix() object to json format
    rows = source_matrix.rows
    cols = source_matrix.cols
    matrix = {"rows": rows, "cols": cols}
    matrix_as_json = json.dumps(matrix, indent=4)

    # store Matrix() in db with an id specific to user
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("INSERT INTO matricies (user_id, matrix) VALUES (?, ?)", 
                                            (user_id, matrix_as_json))
    conn.commit()
    cur.close()
    conn.close()
    
    return matrix_as_json


# Second is:
# --------------------------- #
#     BLUEPRINT TO MATRIX     #
# --------------------------- #
# get blueprint (json format) from client
blueprint = "../test/input_files/5-5.json"

# get export format from user
export_format = ".xls"
# get corresponding source Matrix() from db
conn = sqlite3.connect("../db/matricies.db")
cur = conn.cursor()
cur.execute("SELECT matrix FROM matricies WHERE user_id=?", (user_id,))
json_string = cur.fetchone()[0]
cur.close()
conn.close()
# convert json to matrix object
source_matrix = json_to_matrix(json_string)

# initialize GroupManager with source matrix
gm = GroupManager(source_matrix)
# create groups according to blueprint
gm.build_with()
# export to the wanted format
# return processed file to client


if __name__ == "__main__":
    main()
