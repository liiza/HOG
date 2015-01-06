from flask import Flask
from flask import render_template, request, make_response
from werkzeug import secure_filename, FileStorage

from PIL import Image
from math import sqrt


import os
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+"/tmp"
MAX = sqrt(pow(255, 2) + pow(255, 2))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert_file", methods=["POST"])
def hog():
    print "converting file"
    file = request.files["file"]
    file_name = secure_filename(file.filename)
    print "Got image " + file_name
    image = Image.open(file.stream).convert("LA")
    print "image opened"
    data = image.load()
    # Copy image to reatain the original
    print "Data loaded"
    image_copy = image.copy()
    data_copy =  image_copy.load()
    print "images copied"
    width, height = image.size
    print "image width " + str(width) + " height " + str(height)
    for y in range(1, height - 1):
        for x in range(1, width - 1):
	    #print data_original[x, y][0],
	    value_right = data[x + 1, y][0]
	    value_left = data[x - 1, y][0]
	    I_x = abs(value_right - value_left)
	       
	    value_upper = data[x, y + 1][0]
	    value_down = data[x, y - 1][0]
	    I_y = abs(value_upper - value_down)
	       
	    G = sqrt(pow(I_x, 2) + pow(I_y, 2))
	       
	    G = int(G/MAX*255)
	    data_copy[x, y] = (G, 255)
	    print G,
	       
	print "\n"
    image_copy.save("image_HOG.png")
	    
    print "ready"
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
