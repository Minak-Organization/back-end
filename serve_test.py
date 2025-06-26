from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route("/audio/<filename>")
def serve_audio(filename):
    audio_dir = os.path.join(os.getcwd(), "static", "audio")
    return send_from_directory(audio_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)