from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import csv


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route("/upload")
def upload_data():
    return "upload"


@app.route("/save")
def save_date():
    return "save"


@app.route("/predict", methods=['POST'])
def model_predict():
    return "predicting"


@app.route("/result")
def model_result():
    return "result"


if __name__ == '__main__':
    app.run()
