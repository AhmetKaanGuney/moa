import os

from flask import (
    abort,
    Flask,
    flash,
    json,
    make_response,
    render_template,
    request,
    redirect,
    session,
    send_from_directory,
    url_for,
)

from session_id import SessionID
from matrix_processor import matrix_processor as mp
from matrix_processor import notification as n
from matrix_processor import matrix

CWD = os.getcwd()

app = Flask("app")
app.config.from_pyfile("config.py")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        session["id"] = SessionID.generate()
        return render_template("index.html", session=session)

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
            #!error
            abort(404)

        # Check form data
        matrix_input = {
            "rows": (int(request.form["first-row"]), int(request.form["last-row"])),
            "cols": (request.form["first-col"], request.form["last-col"]),
        }

        print("Checking Form...")

        for k in matrix_input:
            print("Matrix Form: ")
            print(f"{k}: {matrix_input[k]}")
            if matrix_input[k][0] == "" or matrix_input[k][1] == "":
                #!error
                abort(404)

        print("Checking Filename...")
        # check if the post request has the file part
        if "file-input" not in request.files:
            return redirect(request.url)

        # Check if any file is selected
        f = request.files["file-input"]
        if f.filename == "":
            return redirect(request.url)

        if f:
            print("File is Valid...")
            matrix_coords = matrix.coordinates(
                matrix_input["rows"], matrix_input["cols"]
            )

            print("Converting File to Blueprint...")
            # Get file stream
            file_stream = f.stream.read()
            source_blueprint = mp.get_blueprint_from_file(
                file_stream, matrix_coords, session_id
            )

            if source_blueprint == "ERROR":
                #!error
                return n.Notification.error_message, 400

            bp = json.loads(source_blueprint)

            # TODO Delete old files at /downloads
            print("Returning Bleuprint...")

            # Render blueprint page
            return render_template("blueprint.html", blueprint=bp)

        else:
            return redirect(request.url)


@app.route("/blueprint.html", methods=["POST"])
def blueprint():
    if request.method == "POST":
        # Check input
        data = request.get_json()

        print("Checking Request Data...")
        try:
            # Get blueprint
            blueprint = data["blueprint"]

            # Get file format
            file_format = data["fileFormat"]
            if file_format not in ("xlsx", "xls", "csv"):
                abort(404)
        except KeyError:
            abort(404)

        filename = generate_filename(session["id"], file_format)
        path = app.config["DOWNLOAD_FOLDER"] + filename

        print("Writing Blueprint to File...")
        # write bluprint to file
        mp.write_blueprint_to_file(blueprint, file_format, session["id"], file_path=path)

        # Create a url for written file
        url = url_for("download", filename=filename)
        print(f"Generating URL for File: {url}")
        print("Returning Response...")
        # Return the url for the file as response
        return make_response({"status": "OK", "download_url": f"{url}"})


# Handle download request
@app.route("/download/<filename>")
def download(filename):

    print("Checking ID...")
    if "id" not in session:
        return "No session detected."

    print(f"Checking if '{filename}' exists...")
    directory = app.config["DOWNLOAD_FOLDER"]
    path = directory + filename
    if os.path.exists(path):
        print(f"PATH: {path} exists...")
        print(f"Sending '{filename}' from Directory...")
        return send_from_directory(directory, filename)
    else:
        print("Couldn't find file!")
        abort(404)


def read_txt_file(file):
    data = ""
    with open(file, "rb", encoding="utf-8") as f:
        for line in f.readlines():
            data += line
    return data

def generate_filename(session_id, extension):
    return str(session_id) + "." + extension


if __name__ == "__main__":
    app.run()
