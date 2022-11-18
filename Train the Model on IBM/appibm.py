# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:42:22 2022

@author: ELCOT
"""

from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("demo2"))
            arr.append(float(val))

        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        API_KEY = "bCXvySy5lA_FhMbA9k2tNasGQq_8lh6dy9S3-6bBf9pX"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
         API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        payload_scoring = {
            "input_data": [{"fields":[  'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], 
                            "values": [arr]
                            }]
                        }


        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a6665c3d-1be4-4a52-90de-e92572505a25/predictions?version=2022-11-12',json=payload_scoring,headers=header).json()
        
        result = response_scoring['predictions'][0]['values']
        
        if result[0][0] > 0.5:
            return redirect(url_for('chance', percent=result[0][0]*100))
        else:
            return redirect(url_for('nochance', percent=result[0][0]*100))
    else:
        return redirect(url_for("demo2"))

@app.route("/home")
def demo2():
    return render_template("demo2.html")

@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("nochance.html", content=[percent])

@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("demo2"))

if __name__ == "__main__":
    app.run(debug=True)