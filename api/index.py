# for basic API
from flask import Flask, render_template, request, jsonify

# for image conversion
import numpy as np

# for image operations
import cv2 as cv

# import Tracey class
from tracey import Tracey

# initialize app
app = Flask(__name__)

# index api route
@app.route('/')
def index():
    return render_template('index.html')

# route to get paths from an image
@app.route('/paths', methods=['POST'])
def sketch():

    params = {}

    if request.args.get('trace_type'):
        params['trace_type'] = request.args.get('trace_type')

    if request.args.get('threshold_type'):
        params['threshold_type'] = request.args.get('threshold_type')

    if request.args.get('threshold_value'):
        params['threshold_value'] = int(request.args.get('threshold_value'))

    if request.args.get('min_edge_value'):
        params['min_edge_value'] = int(request.args.get('min_edge_value'))

    if request.args.get('max_edge_value'):
        params['max_edge_value'] = int(request.args.get('max_edge_value'))

    if request.args.get('min_path_area'):
        params['min_path_area'] = int(request.args.get('min_path_area'))

    if request.args.get('max_path_area'):
        params['max_path_area'] = int(request.args.get('max_path_area'))

    if request.args.get('path_complexity'):
        params['path_complexity'] = float(request.args.get('path_complexity'))

    if request.args.get('stroke_width'):
        params['stroke_width'] = int(request.args.get('stroke_width'))

    # handle incoming image file
    f = request.files['image'].read()

    # convert image string data to numpy array
    np_img = np.fromstring(f, np.uint8)

    # convert numpy array to image
    img = cv.imdecode(np_img, cv.IMREAD_COLOR)

    # create instance of Tracey class with request params
    t = Tracey(img, params)

    # convert image to grayscale
    t.to_grayscale()

    # blur image with median blur
    t.blur(5)

    # get black/white threshold
    if (t.trace_type == 'threshold' or t.trace_type == 'both'):
        t.get_threshold()

    # extract edges from image
    if (t.trace_type == 'edges' or t.trace_type == 'both'):
        t.get_edges()

    t.get_contours()
    t.smooth_contours()

    t.get_paths()

    # build a response dict to send back to client
    response = {
        'dimensions': {
            'width': t.width,
            'height': t.height
        },
        'paths': t.paths
    }

    return jsonify(response)