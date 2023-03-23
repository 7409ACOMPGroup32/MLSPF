from flask import Flask
from flask_cors import CORS
import sys
import optparse
import time
from flask import request
import sys
from finbert.finbert import predict
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
from transformers import AutoModelForSequenceClassification
import nltk
import os
import ast


# nltk.download('punkt')
# app = Flask(__name__)
# CORS(app)
# start = int(round(time.time()))
# model = BertForSequenceClassification.from_pretrained('/src/models/classifier_model/finbert-sentiment', num_labels=3, cache_dir=None)
model = AutoModelForSequenceClassification.from_pretrained('C:/Users/13862/Desktop/ELEC0136_Final_assignment/final-assignment-Zhao-Mingyang-main/Data_Preprocessing/FIN_BERT/finBERT-master/classifier_model/', num_labels=3, cache_dir=None)

# @app.route("/",methods=['POST'])
def score():
    text='Stocks rallied and the British pound gained.'
    #     request.get_json()['text']
    # print(text)
    return(predict(text, model).to_json(orient='records'))

if __name__ == '__main__':
    output=score()
    # for i in range(len(output["logit"])):
    output = ast.literal_eval(output)[0]
    for i in range(len(output['logit'])):
        print(output['logit'][i])
    # print(output)
    print(output["prediction"])
#     app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
