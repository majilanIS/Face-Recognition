from flask import Blueprint, request, jsonify
from database import get_connection
from face_engine import encode_face, compare_faces
import numpy as np
import tempfile

recognize_bp = Blueprint("recognize", __name__)

@recognize_bp.route("/recognize", methods=["POST"])
def recognize_citizen():
    """
    Expects form-data:
    - face_image (file)
    """
    face_image = request.files.get("face_image")
    if not face_image:
        return jsonify({"error": "No image uploaded"}), 400

    # Save temporarily
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    face_image.save(tmp.name)

    unknown_encoding = encode_face(tmp.name)
    if unknown_encoding is None:
        return jsonify({"error": "No face detected"}), 400

    # Load known faces from DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, national_id, face_encoding FROM citizens")
    citizens = cursor.fetchall()
    cursor.close()
    conn.close()

    for cid, name, national_id, face_blob in citizens:
        known_encoding = np.frombuffer(face_blob, dtype=np.float64)
        match = compare_faces([known_encoding], unknown_encoding)
        if match[0]:
            return jsonify({"id": cid, "name": name, "national_id": national_id}), 200

    return jsonify({"message": "No match found"}), 404