import json
from logging import FileHandler,WARNING
import random
import requests
from datetime import datetime
from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


app = Flask(__name__, static_url_path="", static_folder="static")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/sent/", methods=['POST'])
def send_form():
    id = random.randint(9999, 999999)
    long_url = request.form.get("long_url")
    HTTP_LOGIC_APP = "https://prod-02.northcentralus.logic.azure.com:443/workflows/472d520b360c4f8e8a0bb6f0ed0af76f/triggers/request/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Frequest%2Frun&sv=1.0&sig=UQ76AMjGyzFqjZHTlIUybvYqDZMKJQnozAnDexjUXvY"
    sent_request = requests.post(HTTP_LOGIC_APP, json={"long_url": long_url, "id": id})
    str_id = f'{id}'
    print("OUTGOING-- " + str_id+ " --" + long_url)
    print(sent_request.status_code)
    return render_template('index.html', mylong_url=sent_request.text)


@app.route("/api/receive", methods=['POST'])
def receive_response():  
    if request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            response_json = request.json
            print( "Received HTTP Request")
            print(response_json['long_url'])
            received_long_url = response_json['long_url']
            #return redirect(url_for('index.html', long_url=received_long_url))
            return render_template('index.html', mylong_url=received_long_url)
        return "ACCESS NOT ALLOWED"
    return "ACCESS NOT ALLOWED"

'''
@app.route("/api/receive/", methods=['POST'])
def receive_response():  
    if request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            response_json = request.json
            print( "Received HTTP Request")
            print(response_json['long_url'])
            received_long_url = response_json['long_url']
            #return redirect(url_for('index.html', long_url=received_long_url))
            return render_template('index.html', mylong_url=received_long_url)
        return "ACCESS NOT ALLOWED"
    return "ACCESS NOT ALLOWED"


@app.route('/', methods=['POST'])
def result():
    print(request.form['foo']) # should display 'bar'
    return 'Received !' # response to your request.

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))
'''

if __name__ == '__main__':
    app.run()