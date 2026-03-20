import face_recognition
import numpy as np

def encode_face(image_path):
    """
    Load an image and return face encoding
    """
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        return encodings[0]
    else:
        return None

def compare_faces(known_encodings, unknown_encoding, tolerance=0.5):
    """
    Compare unknown_encoding to a list of known encodings
    Returns True if any match
    """
    results = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=tolerance)
    return results