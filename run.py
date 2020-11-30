from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from ocr import ocr_core

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = '.\\static\\uploads'
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ["PNG", "JPEG", "JPG"]
app.config['MAX_IMAGE_FILESIZE'] = 0.5 * 1024 * 1024


def allowed_image(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)

            image.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))

            addr = f"{app.config['IMAGE_UPLOADS']}\{filename}"

            result = ocr_core(addr)
            outputs = result.splitlines()
            return render_template("upload_image.html", outputs=outputs, addr=addr)

            # return redirect(request.url)

    return render_template("upload_image.html")


if __name__ == "__main__":
    app.run()
