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

# If Website is called normally
@app.route("/")
def home():
    return render_template('index.html')

# If Website is called through POST REQUEST 
# (long url has been entered and sent)
@app.route("/", methods=['POST'])
def send_form():
    id = random.randint(9999, 999999)
    long_url = request.form.get("long_url")
    #Call of API MANAGEMENT to execute logic app
    API_URL = "https://apimanagementccshortener.azure-api.net/LogicApp/logicapp"
    header = {"Ocp-Apim-Subscription-Key": "8d0c0f605b874d7dbb26f29b3a003256"}
    sent_request = requests.post(API_URL, headers=header, json={"long_url": long_url, "id": id})
    # waiting for response as json
    response_body = sent_request.json()
    
    if (id == response_body['id']):
        # getting the long url from the API response
        requested_long_url = response_body['long_url']
        # IF the status is invalid, the long url was not a valid url and we show an error message
        if(response_body['status'] == "invalid"):
            print("URL: " + requested_long_url)
            return render_template('index.html', error_url=requested_long_url)
        # IF status is valid the short url should be displayed on our index.html
        elif(response_body['status'] == "valid"):
            requested_short_url = response_body['short_url']
            print("URL: " + requested_short_url)
            # returns the index.html with filled out fields for short url and long url
            return render_template('index.html', success_short_url=requested_short_url, long_url = requested_long_url)
    else:
        return render_template('index.html')  


# IF website is called with an shortcode behind the /, 
# this method executes
@app.route("/<shortcode>")
def router(shortcode): 
    # CALL OF API MANAGEMENT to execute the azure function for getting the long url matching our short url
    API_URL = "https://apimanagementccshortener.azure-api.net/fetchDB/FetchDBTrigger"
    header = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": "8d0c0f605b874d7dbb26f29b3a003256"}
    sent_request = requests.post(API_URL, headers=header, json={"short_url": shortcode})
    # waiting for response of API call
    response_body = sent_request.content
    # since the content is of datatype 'byte', it is transformed to a string
    link = response_body.decode('utf-8')
    # redirect user to the long url
    return redirect(link)    

if __name__ == '__main__':
    app.run(debug=True)