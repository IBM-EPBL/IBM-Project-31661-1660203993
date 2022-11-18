# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from flask import Flask, render_template, redirect, url_for, request
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "bCXvySy5lA_FhMbA9k2tNasGQq_8lh6dy9S3-6bBf9pX"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
@app.route('/')
def home():
    return render_template("main.html")

@app.route("/predict", methods = ['POST'])
def predict():
    gre = request.form["GRE Score"]
    toefl= request.form["TOEFL Score"]
    u_rate= request.form["University Rating"]
    sop= request.form["SOP"]
    lor= request.form["LOR"]
    cgpa= request.form["CGPA"]
    research= request.form["Research"]
    
    pre=[float(gre),float(toefl),float(u_rate),float(sop),float(lor),float(cgpa),float(research)]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [ 'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], "values": pre}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a6665c3d-1be4-4a52-90de-e92572505a25/predictions?version=2022-11-12', json=payload_scoring,
                                     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred=response_scoring.json()
    print(pred)
    result = pred['predictions'][0]['values'][0][0]
    result = pred['predictions'][0]['values'][0][0]

    if result[0][0] > 0.5:
        return redirect("/chance", percent=result[0][0]*100)
    else:
            return redirect("/nochance", percent=result[0][0]*100)


@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("nochance.html", content=[percent])


if __name__ == "__main__":
    app.run(debug=True)