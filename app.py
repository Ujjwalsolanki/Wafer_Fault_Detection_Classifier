import sys
from flask import Flask, request, render_template
from pathlib import Path
from flask_cors import CORS, cross_origin

from logger import logging

# from src.pipeline.predict_pipeline import PredictPipeline, CustomData
from predict_data_insertion import PredValidation

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
            return render_template('prediction.html',results=results[0])

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
                results = predict_result(path)
                return render_template('prediction.html',results=results[0])

    except Exception as e:
        raise e

def predict_result(path: Path):
    try:
        pred_data_validation = PredValidation(path)
        pred_val = pred_data_validation.initiate_prediction_validation() 

        return pred_val

    except Exception as e:
        logging.exception(e)
        raise e

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)