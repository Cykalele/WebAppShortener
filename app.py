import json
from urllib import response
from urllib.parse import urlunparse
from urllib. request import urlopen
import pymongo
from logging import FileHandler,WARNING
import random
import requests
from datetime import datetime
from distutils.log import debug
from flask import Flask, render_template, request,redirect, url_for, send_from_directory

app = Flask(__name__, static_url_path="", static_folder="static")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def send_form():
    id = random.randint(9999, 999999)
    long_url = request.form.get("long_url")
    #HTTP_LOGIC_APP = "https://prod-02.northcentralus.logic.azure.com:443/workflows/472d520b360c4f8e8a0bb6f0ed0af76f/triggers/request/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Frequest%2Frun&sv=1.0&sig=UQ76AMjGyzFqjZHTlIUybvYqDZMKJQnozAnDexjUXvY"
    API_URL = "https://apimanagementccshortener.azure-api.net/LogicApp/logicapp"
    header = {"Ocp-Apim-Subscription-Key": "8d0c0f605b874d7dbb26f29b3a003256"}
    sent_request = requests.post(API_URL, headers=header, json={"long_url": long_url, "id": id})
    #sent_request = requests.post(HTTP_LOGIC_APP, json={"long_url": long_url, "id": id})
    response_body = sent_request.json()
    
    if (id == response_body['id']):
        requested_long_url = response_body['long_url']
        if(response_body['status'] == "invalid"):
            print("---------------------")
            print("INCOME: IDs are equal")
            print("URL: " + requested_long_url)
            print("---------------------")
            return render_template('index.html', error_url=requested_long_url)
        elif(response_body['status'] == "valid"):
            requested_short_url = response_body['short_url']
            print("---------------------")
            print("INCOME: IDs are equal")
            print("URL: " + requested_short_url)
            print("---------------------")
            return render_template('index.html', success_short_url=requested_short_url, long_url = requested_long_url)
    else:
        return render_template('index.html')  


@app.route("/<shortcode>")
def router(shortcode): 
    API_URL = "https://apimanagementccshortener.azure-api.net/fetchDB/FetchDBTrigger"
    header = {"Content-Type": "application/json","Ocp-Apim-Subscription-Key": "8d0c0f605b874d7dbb26f29b3a003256"}
    sent_request = requests.post(API_URL, headers=header, json={"short_url": shortcode})
    response_body = sent_request.content
    link = response_body.decode('utf-8')
    print(type(link))
    return redirect(link)

if __name__ == '__main__':
    app.run(debug=True)