import os
import pickle
from datetime import datetime
import numpy as np
import pandas as pd
import joblib

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn import preprocessing

from config import Config
from prediction_notes import sales_detail, \
    sales_title, cust_detail, cust_title, time_detail, \
    time_title, analysis_detail, analysis_title, business_questions

columns = ["Customers", "Open", "Promo", "Promo2",

           "StateHoliday", "SchoolHoliday", "CompetitionDistance",
           ""
           "Date", "StoreType", "Assortment", ]

app = Flask(__name__)
app.config.from_object(Config)


class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        try:
            return super().find_class(__name__, name)
        except AttributeError:
            return super().find_class(module, name)


# model = CustomUnpickler(open("models/sales_forecast.pkl", 'rb')).load()

# model = joblib.load("models/sales_forecast.pkl")


# other web views

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route("/about_project", methods=['GET'])
def about_project():
    pred_model = "Serve Model"
    return render_template("about.html", model=pred_model)


# predictions and analysis views

@app.route("/analysis", methods=['GET'])
def analysis():
    return render_template("analysis.html", prediction_name=analysis_title,
                           prediction_detail=analysis_detail,
                           business_questions=business_questions)


@app.route("/predict_sales", methods=['POST'])
def predict_sales():
    if request.method == 'POST':
        store_file = request.files["store-data-file"]
        train_file = request.files["train-data-file"]

    if not train_file and store_file:
        return render_template("upload_error.html", label="No File")

    #   predict_model = joblib.load("models/sales_forecast.pkl")

    return render_template("prediction.html", prediction=type(train_file))


@app.route("/time_series", methods=['POST'])
def time_series():

    if request.method == "POST":

        print("h")

    return render_template("time_series.html", prediction_name=time_title,
                           prediction_detail=time_detail)


@app.route("/pred_charts", methods=['GET'])
def pred_charts(ana_type):
    return render_template("pred_charts.html")


if __name__ == '__main__':
    model = joblib.load("models/sales_forecast.pkl")
    app.run(host="localhost", port=3030)
