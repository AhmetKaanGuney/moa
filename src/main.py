import logging

ENCODING = "UTF-8"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(message)s")
file_handler = logging.FileHandler("../test/logs/test.log", mode="a", encoding=ENCODING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 


# Entry Point
def main():
    pass


if __name__ == "__main__":
    main()
