import logging
from gui.gui_mainloop import run_mainloop

ENCODING = "UTF-8"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(message)s")
file_handler = logging.FileHandler("../test/logs/test.log", mode="a", encoding=ENCODING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# How this program works :
# user sends file to server
# server reads it and returns a blueprint which only contains source file's row and col names
# user groups these names
# user submits the blueprint
# server processes source file's matrix data according to users groupings on the blueprint
# server returns a file containing the new matrix, in the format that user specified

# There are 2 stages of interaction between server and client
# First is called 'Matrix to Blueprint':
# get source file from client
# convert file to Matrix() object
# store Matrix() in db with an id specific to user
# convert Matrix() object to json format
# return blueprint json to client

# Second is called 'Blueprint to Matrix':
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
