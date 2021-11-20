import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    send_from_directory,
)
import flask
from matrix_processor import notification as n

from session_id import SessionID
from matrix_processor import matrix_processor as mp
from matrix_processor import matrix

CWD = os.getcwd()

app = Flask("app")
app.config.from_pyfile("config.py")

# TODO sessions
# TODO name downloads files with user cookie
# TODO on index page get matrix coordinates

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        session["id"] = SessionID.generate()
        print(f"{session.items()=}")
        return render_template("index.html", session=session)

    if request.method == "POST":
        print("Form Data: ")
        # ------------------------- #
        # CHECK USER and USER INPUT #
        # ------------------------- #

        # Do client have an id attached to them
        if "id" in session:
            session_id = session["id"]
        else:
            #!error
            return 404

        # Check form data
        matrix_input = {
            "rows": (int(request.form["first-row"]), int(request.form["last-row"])),
            "cols": (request.form["first-col"], request.form["last-col"])
            }

        for k in matrix_input:
            print(f"{k}: {matrix_input[k]}")
            if matrix_input[k][0] == "" or matrix_input[k][1] == "":
                #!error
                return "bad request!", 404

        print("checking filename...")
        # check if the post request has the file part
        if "file-input" not in request.files:
            return redirect(request.url)

        # Check if any file is selected
        f = request.files["file-input"]
        if f.filename == "":
            return redirect(request.url)

        if f and allowed_file(f.filename):
            print("filename is allowed...")
            matrix_coords = matrix.coordinates(matrix_input["rows"], matrix_input["cols"])

            # temp_filename = app.config["DOWNLOAD_FOLDER"] + f"/{session_id}"
            file_stream = f.stream.read()
            source_blueprint = mp.file_to_blueprint(file_stream, matrix_coords, session_id)

            if source_blueprint == "ERROR":
                #!error
                return n.Notification.error_message, 400
            print(source_blueprint)
            bp = flask.json.loads(source_blueprint)

            # Get file stream
            # binary_data = f.stream.readlines()
            # data = []
            # # Convert binary string to string
            # for line in binary_data:
            #     data.append(line.decode("utf-8"))

            # TODO Delete old files at /downloads

            # Render blueprint page
            return render_template("blueprint.html", blueprint=bp)

        else:
            return redirect(request.url)


# Handle download request
@app.route("/debug.html")
def download_file():
    if "id" not in session:
        return "No session detected."
    return send_from_directory(app.config["DOWNLOAD_FOLDER"])


@app.route("/blueprint.html", methods=["GET", "POST"])
def blueprint():
    if request.method == "GET":
        # TODO
        # source_blueprint = matrix_processor.main("file_to_blueprint", 0)
        # temp_path = f"{CWD}/matrix_processor/test/input_files/source_blueprint.json"
        # with open(temp_path, encoding="utf-8") as f:
        #     source_blueprint = flask.json.load(f)
        # return render_template("blueprint.html", blueprint=source_blueprint)
        return "TODO"


def allowed_file(filename):
    has_dot = "." in filename
    return (
        has_dot
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENTIONS"]
    )


def read_txt_file(file):
    data = ""
    with open(file, "rb", encoding="utf-8") as f:
        for line in f.readlines():
            data += line
    return data


if __name__ == "__main__":
    app.run()
