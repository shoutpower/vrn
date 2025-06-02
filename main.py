from flask import Flask, request, render_template, send_from_directory, url_for
import os
import uuid

app = Flask(__name__)
UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f = request.files["file"]
        if not f:
            return render_template("index.html", obj_url=None)
        uid = str(uuid.uuid4())
        in_path = os.path.join(UPLOAD_DIR, uid + ".jpg")
        out_path = os.path.join(RESULT_DIR, uid + ".obj")
        f.save(in_path)

        # generate dummy .obj result (replace with real VRN call)
        with open(out_path, "w") as obj:
            obj.write("# Dummy face\nv 0 0 0\nv 1 0 0\nv 1 1 0\nf 1 2 3")

        obj_url = url_for("result_file", filename=uid + ".obj")
        full_url = request.host_url.strip("/") + obj_url
        return render_template("index.html", obj_url=obj_url, full_url=full_url)
    return render_template("index.html")

@app.route("/results/<filename>")
def result_file(filename):
    return send_from_directory("results", filename)

if __name__ == "__main__":
    app.run()
