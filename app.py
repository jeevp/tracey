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
    r = request

    # f = r.files.get('image', False)
    f = request.files['image'].read()

    # print(file)

    # img = cv.imread(f,0)

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
    (thresh, sketch) = cv.threshold(sketch, 240, 255, cv.THRESH_BINARY)
    #sketch = cv.multiply(sketch, np.array(bg), scale=(1./128))

    cv.imwrite("final.png", sketch)




    h, w = sketch.shape[:2]

    img = cv.medianBlur(sketch,5)

    # final = Image.fromarray(img)
    # final.show()
    
    # return Response(response={"hello": "there"}, status=200, mimetype="application/json")
    
    th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
                cv.THRESH_BINARY_INV,11,2)

    th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv.THRESH_BINARY_INV,11,2)

    # (thresh, sketch) = cv.threshold(sketch, 240, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(th3, cv.RETR_EXTERNAL , cv.CHAIN_APPROX_TC89_L1)

    # c = max(contours, key=cv.contourArea) #max contour

    svg_text = f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'

    for c in contours:
        area = cv.contourArea(c)
        if area > 20:
            svg_text += '<path d="M'
            for i in range(len(c)):
                x, y = c[i][0]
                svg_text += f"{x} {y} "
            
            if area > 60:
                svg_text += ' " fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
            else:
                svg_text += ' " fill="black" stroke="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'


    # (thresh_inv, sketch_inv) = cv.threshold(sketch, 240, 255, cv.THRESH_BINARY_INV)
    # contours_inv, hierarchy_inv = cv.findContours(sketch_inv, cv.RETR_EXTERNAL , cv.CHAIN_APPROX_TC89_L1)

    # for c in contours_inv:
    #     area = cv.contourArea(c)
    #     if area > 3 and area / (w*h) < 0.5:
    #         f.write('<path d="M')
    #         for i in range(len(c)):
    #             x, y = c[i][0]
    #             f.write(f"{x} {y} ")
    #         f.write(' " fill="none" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n')



    # f.close()

    svg_text += "</svg>"
    print("DONE")

    # # build a response dict to send back to client
    response = {'contents': svg_text}

    return jsonify(response)
    # return Response(response={"hello": "there"}, status=200, mimetype="application/json")