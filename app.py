import sys, os
from signLanguage.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)   

# Enable CORS

cors = CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/predict",methods = ['POST','GET'])
@cross_origin
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image,ClientApp.filename)
        os.system("cd yolov5/ &&  python detect.py --weights best.pt --img 416 --conf 0.5 --source 0 ")

        opencodedbase64 = encodeImageIntoBase64("yolov5/runs/detect/exp/inputImage.jpg")
        result = {"image":opencodedbase64.decode('utf-8')}
        os.system("rm -rf yolov5/runs")

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"
    return jsonify(result)