from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    send_from_directory,
)
from session_id import SessionID

# import matrix_processor


app = Flask("app")
app.config.from_pyfile("config.py")

# TODO sessions
# TODO name downloads files with user cookie


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


@app.route("/", methods=["GET"])
def homepage():
    return redirect("upload.html")


@app.route("/upload.html", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        session["id"] = SessionID.generate()
        print(f"{session.items()=}")
        return render_template("upload.html", session=session)

    if request.method == "POST":
        print("uplodad file")
        print("REQUEST FILE: ", request.files)

        # Do client have an id attached to them
        if "id" in session:
            session_id = session["id"]
        else:
            return 404

        # Upload file
        # check if the post request has the file part
        if "file_input" not in request.files:
            return redirect(request.url)

        # Check if any file is selected
        f = request.files["file_input"]
        if f.filename == "":
            flash("No file selcted.")
            return redirect(request.url)

        if f and allowed_file(f.filename):
            print("filename is allowed")
            # Get file stream
            binary_data = f.stream.readlines()
            data = []
            # Convert binary string to string
            for line in binary_data:
                data.append(line.decode("utf-8"))

            # Delete old files at /downloads

            # Write to file
            temp_filename = app.config["DOWNLOAD_FOLDER"] + f"/{session_id}" + ".txt"
            with open(temp_filename, "w", encoding="utf-8") as temp_f:
                for line in data:
                    temp_f.write(line)

            # Render download page
            return render_template("download.html", data=data, session=session)

        else:
            return redirect(request.url)


# Handle download request
@app.route("/download_file")
def download_file():
    if "id" not in session:
        return "No session detected."
    name = session["id"]
    ext = ".txt"
    filename = str(name) + ext
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename)


@app.route("/blueprint.html", methods=["GET", "POST"])
def blueprint():
    if request.method == "GET":
        return render_template("blueprint.html")


if __name__ == "__main__":
    app.run()
