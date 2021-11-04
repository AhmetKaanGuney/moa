from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
import io
# import file_exchange

app = Flask("app")
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config.from_pyfile("config.py")
ALLOWED_EXTENTIONS = {"txt", "xls", "xlsx", "csv", "json"}
print("secret key : ", app.secret_key)


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENTIONS

def read_txt_file(file):
    data = ""
    with open(file, "rb", encoding="utf-8") as f:
        for line in f.readlines():
            data += line
    return data

@app.route("/", methods=["GET"])
def mainpage():
    return redirect("index.html")

@app.route("/index.html", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        print("uplodad file")
        print("REQUEST FILE: ", request.files)
        # Upload file
        # check if the post request has the file part
        if "source_file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        f = request.files["source_file"]
        if f.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if f and allowed_file(f.filename):
            print("filename is allowed")
            binary_data = f.stream.readlines()
            data = []
            for line in binary_data:
                data.append(line.decode("utf-8"))
            print("data: ", data)
            return render_template("upload.html", data=data)
