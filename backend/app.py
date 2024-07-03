import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from time import sleep
import base64
from PIL import Image, ImageChops
from io import BytesIO
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/screenshot', methods=['POST'])
def screenshot():
    try:
        screenshotData = request.json
        index = screenshotData['index']
        url = screenshotData['url']
        is_empty = screenshotData['is_empty']
        # we keep the actual image url
        base64_img = url.split(',')[1]
        # convert it to an actual image
        screenshot = base64.b64decode(base64_img)
        """
        Some images took WAY longer (up to 4 min) than others so i had to
        check in some way if the screenshot actually got the graph or not
        """
        # checking if graph is empty by comparing it to an empty one
        img1 = Image.open(BytesIO(screenshot))
        # if the original frame is not blank, we check if the screenshot is blank
        if (not(is_empty)):
            img2 = Image.open("./empty_screenshots_templates/desmos_empty.png")
            if np.sum(np.array(ImageChops.difference(img1, img2).getdata())) == 0:
                print("taking ss again")
                return jsonify({'message': f'screenshot {index} is empty, take again.'}), 400
        # totally blank graph is always bad
        img3 = Image.open("./empty_screenshots_templates/blank_graph.png")
        if np.sum(np.array(ImageChops.difference(img1, img3).getdata())) == 0:
            print("taking ss again")
            return jsonify({'message': f'screenshot {index} is empty, take again.'}), 400
        path = f"../frames/desmosframes/desmosframe{index}.png"
        with open(path, 'wb') as frame: frame.write(screenshot)
        return jsonify({'message': f'screenshot {index} uploaded successfully.'}), 200
    
    except Exception as e:
        return jsonify({'message': f'error with screenshot {index}, {str(e)}'}), 500
    
@app.route('/element')
def get_element():
    index = request.args.get('index', type=int)
    
    if index == -1: return jsonify({"num of frames": num_frames})
    elif (index is not None) and (0 <= index < num_frames): return jsonify(server_frames[index])
    return jsonify({"error": "Index out of range"}), 400

if __name__ == '__main__':
    
    frames = open("../frames/serverframes.json")

    server_frames = json.load(frames)

    num_frames = len(server_frames)
    
    print("Copyright © 2024 [shrimp](https://github.com/it0kawa)")
    print("Please provide proper credit to the author (shrimp) in any public use of this software")

    print("\nGET requests at http://127.0.0.1:5000/element?index=<index>")
    print("POST requests at http://127.0.0.1:5000/screenshot")
    app.run()
