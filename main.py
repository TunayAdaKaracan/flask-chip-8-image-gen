import math
from flask import Flask, request, send_file
from PIL import Image, ImageDraw
from io import BytesIO

app = Flask(__name__)


def do_render(scale, data):
    render = Image.new(size=(64 * scale, 32 * scale), mode="1")
    drawer = ImageDraw.Draw(render, mode="1")
    for i in range(64 * 32):
        x = (i % 64) * scale
        y = math.floor(i / 64) * scale
        if data[i] == 1:
            drawer.rectangle((x, y, x+scale-1, y+scale-1), fill=255)
    return render


def decode_data(data):
    unpacked_bits = []
    for byte in data:
        byte = int(byte)
        for i in range(7, -1, -1):
            unpacked_bits.append((byte >> i) & 1)
    return unpacked_bits


@app.route("/")
def index():
    scale = int(request.args.get("scale", 1))
    data = request.args.get("data")
    if data is None:
        return ""
    data = data.split(",")
    
    if len(data) != 256:
        return ""

    data = decode_data(data)

    render = do_render(scale, data)
    img_io = BytesIO()
    render.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
