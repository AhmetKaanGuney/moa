import os
import time
import secrets

from flask import (
    Flask,
    json,
    make_response,
    render_template,
    request,
    session,
    send_from_directory,
    url_for,
)

from session_id import SessionID
from matrix_processor import matrix_processor as mp
from matrix_processor.errors import Error
from matrix_processor import matrix

CWD = os.getcwd()

app = Flask("app")
app.config.from_pyfile("config.py")


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "GET":
        session["id"] = SessionID.generate()
        return render_template("index.html")

    if request.method == "POST":
        print("Getting Form...")
        # ------------------------- #
        # CHECK USER and USER INPUT #
        # ------------------------- #

        print("Checking ID...")

        # Do client have an id attached to them
        if "id" in session:
            session_id = session["id"]
        else:
            error = "No ID detected!"
            return render_template("index.html", error=error)

        print("Checking Form...")
        # Check form data
        for i in (
            request.form["first-row"],
            request.form["last-row"],
            request.form["first-col"],
            request.form["last-col"],
        ):
            if i == "":
                error = "All fields must be filled."
                return render_template("index.html", error=error)

        # Assigning input data
        matrix_input = {
            "rows": (int(request.form["first-row"]), int(request.form["last-row"])),
            "cols": (request.form["first-col"], request.form["last-col"]),
        }

        print("Checking Filename...")
        # check if the post request has the file part
        if "file-input" not in request.files:
            error = "All fields must be filled."
            return render_template("index.html", error=error)

        # Check if any file is selected
        f = request.files["file-input"]
        if f.filename == "":
            error = "Invalid name for file."
            return render_template("index.html", error=error)

        if f:
            print("File is Valid...")
            matrix_coords = matrix.coordinates(
                matrix_input["rows"], matrix_input["cols"]
            )

            print("Converting File to Blueprint...")
            # Get file format
            file_format = f.filename.split('.')[1]
            # Get file stream
            file_stream = f.stream.read()
            try:
                source_blueprint = mp.get_blueprint_from_file(
                    file_stream, file_format, matrix_coords, session_id
                )
            except Exception as e:
                error = e
                return render_template("index.html", error=error)

            if source_blueprint == None:
                error = Error.message
                return render_template("index.html", error=error)

            bp = json.loads(source_blueprint)

            # Delete at DOWNLOADS_FOLRDER
            delete_old_files()

            print("Returning Bleuprint...")
            # Render blueprint page
            return render_template("blueprint.html", blueprint=bp)

        else:
            error = "Invalid file."
            return render_template("index.html", error=error)


@app.route("/blueprint.html", methods=["POST"])
def blueprint():
    error = None
    if request.method == "POST":
        # Check input
        data = request.get_json()

        print("Checking Request Data...")
        try:
            # Get blueprint
            blueprint = data["blueprint"]
            # Get file format
            file_format = data["fileFormat"]
        except KeyError:
            return "Something went wrong", 404

        if file_format not in ("xlsx", "xls"):
            error = "Invalid file format."
            return render_template("blueprint.html", error=error)

        filename = generate_filename(file_format)
        path = app.config["DOWNLOAD_FOLDER"] + filename

        print("Writing Blueprint to File...")
        # write bluprint to file
        try:
            mp.write_blueprint_to_file(
                blueprint, file_format, session["id"], file_path=path
            )
        except Error:
            return make_response({"status": "ERROR", "error": Error.message})

        # Create a url for written file
        url = url_for("download", filename=filename)
        print(f"Generating URL for File: {url}")
        print("Returning Response...")
        # Return the url for the file as response
        return make_response({"status": "OK", "download_url": f"{url}"})


# Handle download request
@app.route("/download/<filename>")
def download(filename):
    error = None

    print("Checking ID...")
    if "id" not in session:
        error = "No ID detected!"
        return render_template("index.html", error=error)

    print(f"Checking if '{filename}' exists...")
    directory = app.config["DOWNLOAD_FOLDER"]
    path = directory + filename
    if os.path.exists(path):
        print(f"PATH: {path} exists...")
        print(f"Sending '{filename}' from Directory...")
        return send_from_directory(directory, filename)
    else:
        error = "No such file exists."
        return render_template("blueprint.html", error=error)


@app.route("/how-to-use.html", methods=["GET"])
def how_to_use():
    if request.method == "GET":
        return render_template("how-to-use.html")


@app.route("/how-to-format.html", methods=["GET"])
def how_to_format():
    if request.method == "GET":
        return render_template("how-to-format.html")


def read_txt_file(file):
    data = ""
    with open(file, "rb", encoding="utf-8") as f:
        for line in f.readlines():
            data += line
    return data


def generate_filename(extension):
    filename = secrets.token_hex(4)
    return filename + "." + extension


def delete_old_files():
    download_folder = app.config["DOWNLOAD_FOLDER"]
    for i in os.listdir(download_folder):
        file_path = download_folder + i
        # in seconds
        time_passed = time.time() - os.path.getmtime(file_path)
        one_hour = 3600
        if time_passed > one_hour:
            os.remove(file_path)


if __name__ == "__main__":
    app.run()
