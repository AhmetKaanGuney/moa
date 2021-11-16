import os

for filename in os.listdir("./"):
    if filename == "names.py":
        continue
    new_name = filename.split("xls_")[1:][0]
    os.rename(filename, new_name)
    print(new_name)