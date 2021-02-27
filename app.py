from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2 as cv
from sketchbook import Sketch
from edges import Edges

from PIL import Image, ImageOps


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sketch', methods=['POST'])
def sketch():

    threshold_type = cv.ADAPTIVE_THRESH_GAUSSIAN_C
    # invert_threshold = cv.THRESH_BINARY

    if request.args.get('threshold_type') is 'mean':
        threshold_type = cv.ADAPTIVE_THRESH_MEAN_C

    if request.args.get('threshold_inversion'):
        threshold_inversion = request.args.get('threshold_inversion')

    if request.args.get('threshold_value'):
        threshold_value = int(request.args.get('threshold_value'))
    if request.args.get('min_fill_area'):
        min_fill_area = int(request.args.get('min_fill_area'))
    if request.args.get('min_path_area'):
        min_path_area = int(request.args.get('min_path_area'))
    if request.args.get('stroke_width'):
        stroke_width = int(request.args.get('stroke_width'))


    print(threshold_type)
    print(threshold_value)
    print(f'invert threshold: {threshold_inversion}')

    f = request.files['image'].read()

    #convert string data to numpy array
    npimg = np.fromstring(f, np.uint8)
    # convert numpy array to image
    img = cv.imdecode(npimg, cv.IMREAD_COLOR)

        
    sketch = Sketch(img).sketch()
    # bg = Background(img.size, octaves=6).background()
    edges = Edges(img).edges()
    #sketchTrans = cv.cvtColor(sketch, cv.COLOR_GRAY2RGBA)

    mask = edges[3]
    sketch = cv.bitwise_and(sketch, edges, edges)
    (thresh, sketch) = cv.threshold(sketch, 240, threshold_value, cv.THRESH_BINARY)
    #sketch = cv.multiply(sketch, np.array(bg), scale=(1./128))

    # cv.imwrite("final.png", sketch)

    h, w = sketch.shape[:2]

    img = cv.medianBlur(sketch,5)

    # final = Image.fromarray(img)
    # final.show()

    

    total_area = w*h

    header = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'

    svg_text = header

    paths = ''
    inverted_paths = ''

    if threshold_inversion == 'both' or threshold_inversion == 'none':
        threshold = cv.adaptiveThreshold(img, threshold_value, threshold_type, cv.THRESH_BINARY, 11,2)
        contours, hierarchy = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)
        # add non-inverted version
        for c in contours:
            area = cv.contourArea(c)
            if (area / total_area) > (min_fill_area / total_area) * 100:
                paths += '<path d="M'
                for i in range(len(c)):
                    x, y = c[i][0]
                    paths += f"{x} {y} "
                
                if (area / total_area) > (min_path_area / total_area) * 100:
                    paths += f' " fill="none" stroke="black" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>\n'
                else:
                    paths += f' " fill="black" stroke="none" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>\n'

    if threshold_inversion == 'both' or threshold_inversion == 'invert':
        # add inverted version
        inverted_threshold = cv.adaptiveThreshold(img, threshold_value, threshold_type, cv.THRESH_BINARY_INV, 11,2)
        inverted_contours, inverted_hierarchy = cv.findContours(inverted_threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_L1)
        for c in inverted_contours:
            area = cv.contourArea(c)
            if (area / total_area) > (min_fill_area / total_area) * 100:
                inverted_paths += '<path d="M'
                for i in range(len(c)):
                    x, y = c[i][0]
                    inverted_paths += f"{x} {y} "
                
                if (area / total_area) > (min_path_area / total_area) * 100:
                    inverted_paths += f' " fill="none" stroke="black" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>\n'
                else:
                    inverted_paths += f' " fill="black" stroke="none" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>\n'


    if threshold_inversion == 'both':
        svg_text += paths
        svg_text += inverted_paths
    elif threshold_inversion == 'invert':
        svg_text += inverted_paths
    else:
        svg_text += paths


    svg_text += "</svg>"
    print("DONE")

    # # build a response dict to send back to client
    response = {'contents': svg_text}

    return jsonify(response)
    # return Response(response={"hello": "there"}, status=200, mimetype="application/json")