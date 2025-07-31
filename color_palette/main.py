import os
from collections import defaultdict

import numpy as np
from PIL import Image
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap5
from matplotlib.colors import to_hex
from werkzeug.utils import secure_filename

app = Flask(__name__)
Bootstrap5(app)
# Create a folder to load image on flask

app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB limit

app.config["UPLOAD_FOLDER"] = "./static"
# Ensure the upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename: str) -> bool:
    """
    Check if the selected file is in a valid image format
    :param filename: File selected by the user
    :return:  Whether the given file is valid or not.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Generate Index page
    """
    filename = ""
    if request.method == "POST":
        filepath = ""
        # Check if the exists
        if "image_file" not in request.files:
            error = "No file part"
        else:
            # Get file from form
            file = request.files["image_file"]
            # Check if a file is selected
            if file.filename == '':
                error = "No selected file"
            # Check if the file is valid
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                error = None
            else:
                error = "File type not allowed"
        return render_template("index.html", image_to_render=filepath, colors=get_common_colors(filepath))
    return render_template("index.html")


def get_common_colors(file: str):
    img = Image.open(file)
    img = img.convert("RGB")
    color_counts = defaultdict(int)

    pixels = list(img.getdata())

    for pixel in pixels:
        color_counts[pixel] += 1

    # Get top N colors
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    color_list = []
    for color in sorted_colors:
        formated_color = np.array(color[0]) / 255
        color_list.append(to_hex(formated_color))
    return color_list


if __name__ == "__main__":
    app.run(debug=True)
