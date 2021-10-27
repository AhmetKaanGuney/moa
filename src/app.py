#! "./venv/Scripts/python.exe"

import logging
import flask
import sqlite3

from file_io import XlsFile
import json
from matrix import Matrix, col_to_num, matrix_coordinates

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
# server returns a file containing the new matrix, in the format that user specified

# There are 2 stages of interaction between server and client

# First is:
# --------------------------- #
#     MATRIX TO BLUEPRINT     #
# --------------------------- #

# get source file and matrix coordinates from client
coordinates = matrix_coordinates((2, 6), ("b", "f"))
source_file = "./test/input_files/5-5.xls"
user_id = 0
# check file type
# convert file to Matrix() object    
source_matrix = XlsFile(source_file, coordinates).parse()
print(source_matrix.name, "\n", 
  source_matrix.get_rows(),"\n", source_matrix.get_cols())

# convert Matrix() object to json format
rows = ""
cols = ""
for name in source_matrix.get_rows():
    rows += name + ","
for name in source_matrix.get_cols():
    cols += name + ","
matrix_as_json = json.dumps({"rows": rows, "cols": cols})
print(matrix_as_json)

# store Matrix() in db with an id specific to user
con = sqlite3.connect("./db/matricies.db")
cur = con.cursor()
cur.execute("INSERT INTO matricies VALUES (user_id=?, matrix=?)", 
                                        user_id, matrix_as_json)

print(cur.excute("SELECT * FROM matricies"))

# return blueprint json to client

# Second is:
# --------------------------- #
#     BLUEPRINT TO MATRIX     #
# --------------------------- #

# get blueprint (json format) from client
# get export format from user
# get corresponding source Matrix() from db
# initialize GroupManager with source matrix
# create groups according to blueprint
# export to the wanted format
# return processed file to client


# Entry Point
def main():
    pass


if __name__ == "__main__":
    main()
