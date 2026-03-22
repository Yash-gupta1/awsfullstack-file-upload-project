from flask import Flask, request, jsonify, render_template_string
import boto3, os

app = Flask(__name__)
BUCKET = "my-gallery-bucket-staticwebsite-2"
s3 = boto3.client("s3", region_name="eu-north-1")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>My Gallery</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; background: #f0f0f0; }
        h1 { color: #333; }
        .upload-box { background: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .gallery img { width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
        button { background: #ff6600; color: white; border: none; padding: 10px 25px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        input[type=file] { margin: 10px 0; }
    </style>
</head>
<body>
    <h1>📸 My File Gallery</h1>
    <div class="upload-box">
        <h3>Upload a File</h3>
        <input type="file" id="fileInput" /><br/>
        <button onclick="uploadFile()">Upload to S3</button>
        <p id="status"></p>
    </div>
    <h3>Uploaded Files:</h3>
    <div class="gallery" id="gallery"></div>
    <script>
        async function uploadFile() {
            const file = document.getElementById('fileInput').files[0];
            if (!file) return alert('Pick a file first!');
            const formData = new FormData();
            formData.append('file', file);
            document.getElementById('status').innerText = 'Uploading...';
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const data = await res.json();
            document.getElementById('status').innerText = data.message;
            loadFiles();
        }
        async function loadFiles() {
            const res = await fetch('/files');
            const data = await res.json();
            const gallery = document.getElementById('gallery');
            gallery.innerHTML = '';
            data.files.forEach(url => {
                const img = document.createElement('img');
                img.src = url;
                img.onerror = function() {
                    this.style.display='none';
                    const p = document.createElement('p');
                    p.innerText = '📄 ' + url.split('/').pop().split('?')[0];
                    gallery.appendChild(p);
                };
                gallery.appendChild(img);
            });
        }
        loadFiles();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    s3.upload_fileobj(file, BUCKET, file.filename)
    return jsonify({"message": f"{file.filename} uploaded successfully!"})

@app.route("/files")
def files():
    response = s3.list_objects_v2(Bucket=BUCKET)
    urls = []
    if "Contents" in response:
        for obj in response["Contents"]:
            url = s3.generate_presigned_url("get_object",
                Params={"Bucket": BUCKET, "Key": obj["Key"]}, ExpiresIn=3600)
            urls.append(url)
    return jsonify({"files": urls})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
