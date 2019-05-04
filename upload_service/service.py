import io

from flask import Flask, jsonify, request, send_file
import pymongo
from werkzeug.utils import secure_filename

app = Flask(__name__)

MONGO_DB_HANDLER = pymongo.MongoClient("mongodb", 27017)
FILE_DB = MONGO_DB_HANDLER["files_db"]
FILES = FILE_DB["files"]


@app.route("/upload", methods=["POST"])
def upload_file():
    folder = request.form['folder']

    files = []

    for file in request.files.getlist("file"):
        filename = secure_filename(file.filename)

        filedata = {
            "folder": folder,
            "filename": filename,
            "data": file.stream.read()
        }

        files.append(filedata)

    result = FILES.insert_many(files)

    return jsonify({"status": "200",
                    "text": f"inserted {len(result.inserted_ids)} files",
                    "added": [f"{folder}::{f['filename']}" for f in files]})


@app.route("/retrieve/<string:folder>/<string:file_name>", methods=["GET"])
def retrieve_file(folder, file_name):
    query = {
        "folder": folder,
        "filename": file_name
    }

    for result in FILES.find(query):
        return send_file(
            io.BytesIO(result["data"]),
            attachment_filename=result["filename"],
            mimetype='application/octet-stream'
        )

    return jsonify({"error": f"File {file_name} at {folder} not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
