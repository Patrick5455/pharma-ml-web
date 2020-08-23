import pickle
from datetime import datetime
from config import Config
import numpy as np
import pandas as pd
from flask import Flask, render_template, flash, redirect, request
from models.model_classes import Preprocessing, Regressor

from prediction_notes import sales_detail, \
    sales_title, cust_detail, cust_title, time_detail, \
    time_title, analysis_detail, analysis_title, business_questions

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def hello_world():
    return render_template('index.html')


columns = ["Customers", "Open", "Promo", "Promo2",

           "StateHoliday", "SchoolHoliday", "CompetitionDistance",
           ""
           "Date", "StoreType", "Assortment", ]


class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        try:
            return super().find_class(__name__, name)
        except AttributeError:
            return super().find_class(module, name)


model = CustomUnpickler(open("models/model1.pkl", 'rb')).load()


# other web views

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", )


@app.route("/about", methods=['GET'])
def about():
    model = "Serve Model"
    return render_template("about.html", model=model)


# predictions and analysis views

@app.route("/predict", methods=['POST'])
def predict():
    # to:do add logic to determine which model to load based the type pf prediction

    model_result = request.form.values()
    # print(model_result)
    features = []
    for val in model_result:
        if "-" in val:
            dt = datetime.strptime(val, '%Y-%m-%d')
            date = dt.date()
            features.append(date)
        else:
            features.append(int(val))
    [print(f, type(f)) for f in features]
    data = np.array(features)
    data = data.reshape(1, len(columns))
    data = pd.DataFrame(data, columns=columns)

    print(data.columns.values)

    data = model.predict(data)

    prediction = model.predict(data)

    return render_template("prediction.html", prediction="prediction")


@app.route("/analysis", methods=['GET'])
def analysis():
    return render_template("analysis.html", prediction_name=analysis_title,
                           prediction_detail=analysis_detail,
                           business_questions=business_questions)


@app.route("/time", methods=['GET'])
def time_series():
    return render_template("time_series.html", prediction_name=time_title,
                           prediction_detail=time_detail)


@app.route("/cust", methods=['GET'])
def cust_churn():
    return render_template("cust_churn.html", prediction_name=cust_title,
                           prediction_detail=cust_detail)


@app.route("/sales", methods=['GET'])
def sales_forecast():
    return render_template("sales_forecast.html", prediction_name=sales_title,
                           prediction_detail=sales_detail)


@app.route("/pred_charts", methods=['GET'])
def show_charts(ana_type):
    return render_template("pred_charts.html")


if __name__ == '__main__':
    app.run()
