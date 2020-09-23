# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 12:25:00 2020

@author: Safoora Naureen
"""

import numpy as np
import pandas as pd
import json
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('compressive_strength.pickle', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    
    features_name = ['Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water', 
                     'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate',
                     'Age', 'wc_ratio']
    
    df = pd.DataFrame(features_value, columns=features_name)
    res_val = model.predict(df)
        
    return render_template('index.html', prediction_text='Compressive Strength is {} MPa'.format(res_val))


@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force = True)
    prediction = model.predict([np.array(list(data.values()))])
    
    output = model.predict(prediction[0])
    return jsonify(output)


if __name__ == "__main__":
    app.run()
