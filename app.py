from wsgiref import simple_server
from flask import Flask, request, render_template
from pathlib import Path
from flask_cors import CORS, cross_origin
from flask import Response
import json
from logger import logging

from predict_data_insertion import PredValidation
from prediction.prediction import Prediction

application = Flask(__name__)
app = application
CORS(app)

@app.route('/', methods=['GET'])
def index():
    try:

        if request.method == 'GET':
            return render_template('index.html')
        else:
            logging.info("prediction post method called")
            path = request.json['filepath']
            predict_result(path)
            return render_template('prediction.html',results=predict_result[0])

    except Exception as e:
        raise e
    
@app.route('/predict', methods=['POST'])
def predict_data():
    try:

        if request.method == 'GET':
            return render_template('index.html')
        else:
            logging.info("prediction post method called")
            if request.json['filepath'] is not None:
                path = request.json['filepath']
                path, result = predict_result(path)

            return Response("Prediction File created at !!! "  +str(path) +' and few of the predictions are '+str(json.loads(result)))    

    except Exception as e:
        raise e

def predict_result(path: Path):
    try:
        pred_data_validation = PredValidation(path)
        pred_data_validation.initiate_prediction_validation()

        prediction = Prediction(path)
        path, result = prediction.predict_from_model()

        return path, result

    except Exception as e:
        logging.exception(e)
        raise e

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
    