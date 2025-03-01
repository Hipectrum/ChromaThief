from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import io
from PIL import Image
from collections import Counter
import tempfile


app = Flask(__name__)

def extract_colors(image, num_colors=10):

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    pixels = image_rgb.reshape(-1, 3)
    color_counts = Counter(map(tuple, pixels))


    most_common_colors = color_counts.most_common(num_colors)

    color_squares = np.zeros((50, num_colors * 50, 3), dtype=np.uint8)

    for i, (color, count) in enumerate(most_common_colors):
        color_squares[:, i * 50: (i + 1) * 50] = color

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    cv2.imwrite(temp_file.name, color_squares)

    return temp_file.name



@app.route("/", methods=["GET", "POST"])
def index():

    colors_image_path = None

    if request.method == "POST":
        file = request.files["file"]
        image = Image.open(io.BytesIO(file.read()))
        image = np.array(image)
        colors_image_path = extract_colors(image, num_colors=10)

    return render_template("index.html", colors_image_path=colors_image_path)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_file(filename)



if __name__ == "__main__":
    app.run(debug=True)