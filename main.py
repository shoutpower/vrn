from flask import Flask, render_template, request, send_from_directory, url_for
import os
import uuid

app = Flask(__name__)
UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return render_template("index.html", obj_url=None)
        uid = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_DIR, uid + ".jpg")
        output_path = os.path.join(RESULT_DIR, uid + ".obj")
        file.save(input_path)

        # Dummy .obj content
        with open(output_path, "w") as f:
            f.write("# Dummy OBJ\nv 0 0 0\nv 1 0 0\nv 1 1 0\nf 1 2 3")

        obj_url = url_for("result_file", filename=uid + ".obj")
        return render_template("index.html", obj_url=obj_url)
    return render_template("index.html", obj_url=None)

@app.route("/results/<filename>")
def result_file(filename):
    return send_from_directory(RESULT_DIR, filename)

if __name__ == "__main__":
    app.run()
