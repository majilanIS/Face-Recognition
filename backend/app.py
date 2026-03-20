from flask import Flask
from routes.register import register_bp
from routes.recognize import recognize_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(register_bp)
app.register_blueprint(recognize_bp)

@app.route("/")
def home():
    return "Face Recognition API is running!"

if __name__ == "__main__":
    app.run(debug=True)