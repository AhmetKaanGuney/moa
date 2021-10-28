"""test for group_manager"""
from converters import Matrix
from group_manager import GroupManager
from converters import XlsFile
import logging
import os
import sys
import unittest

# Go to upper directory and then import files
cwd = os.getcwd()
parentdir = os.path.dirname(cwd)
sys.path.append(parentdir)
print("parent dir: ", parentdir)


ENCODING = "UTF-8"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(message)s")

file_handler = logging.FileHandler(parentdir + "/moa/logs/grup_manager.log",
                                   mode="a", encoding=ENCODING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


try:
    my_log = open(parentdir + "/moa/logs/engine_test.log", "w")
    my_log.write("")
    my_log.close()
except FileNotFoundError:
    pass


class TestGroupManager(unittest.TestCase):

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

