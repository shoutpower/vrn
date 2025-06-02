from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)

HTML = open("index.html", encoding="utf-8").read()

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return 'No file uploaded', 400
    filepath = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)

    # VRN 처리 가정
    output_path = 'face_output.obj'
    with open(output_path, 'w') as f:
        f.write('# dummy obj')

    return render_template_string(HTML + '<br><a href="/download">.obj 다운로드</a>')

@app.route('/download')
def download():
    return send_file('face_output.obj', as_attachment=True)

if __name__ == '__main__':
    app.run()
