from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import requests

app = Flask(__name__, static_url_path="", static_folder="static")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def send_form():
    if request.method == "POST":
        long_url = request.form.get("long_url")
        HTTP_LOGIC_APP = "https://prod-02.northcentralus.logic.azure.com:443/workflows/472d520b360c4f8e8a0bb6f0ed0af76f/triggers/request/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Frequest%2Frun&sv=1.0&sig=UQ76AMjGyzFqjZHTlIUybvYqDZMKJQnozAnDexjUXvY"
        requests.post(HTTP_LOGIC_APP, json={"long_url": long_url})
        
    return render_template('post.html')

'''
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