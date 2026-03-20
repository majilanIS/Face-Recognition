from flask import Blueprint, request, jsonify
from database import get_connection
from face_engine import encode_face
import os

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register_citizen():
    name = request.form.get("name")
    national_id = request.form.get("national_id")
    face_image = request.files.get("face_image")

    if not all([name, national_id, face_image]):
        return jsonify({"error": "Missing data"}), 400

    image_path = f"temp_{national_id}.jpg"
    face_image.save(image_path)

    encoding = encode_face(image_path)
    if encoding is None:
        os.remove(image_path)
        return jsonify({"error": "No face detected"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Check duplicate
    cursor.execute("SELECT * FROM citizens WHERE national_id = %s", (national_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        os.remove(image_path)
        return jsonify({"error": "User already exists"}), 400

    try:
        sql = "INSERT INTO citizens (name, national_id, face_encoding) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, national_id, encoding.tobytes()))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
        os.remove(image_path)

    return jsonify({"message": f"{name} registered successfully!"}), 200