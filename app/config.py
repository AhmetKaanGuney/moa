import json

with open("../env.json") as f:
    ENV = json.load(f)

TEMPLATES_AUTO_RELOAD = True
DOWNLOAD_FOLDER = ENV["DOWNLOAD_FOLDER"]
SECRET_KEY = ENV["SECRET_KEY"]
ALLOWED_EXTENTIONS = {"xls", "xlsx"}
# Allows for total of 500 mb at the /downloads
MAX_CONTENT_LENGTH = 1 * 1000 * 1000    # 1 MBs
