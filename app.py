from flask import Flask, request
import secrets as secrets

import os
import socket

app = Flask(__name__)

port = int(os.environ.get('PORT', 5000))

@app.route("/")
def hello():
    html = "<body style=\"background-color:lightgray;\">" \
           "<h2 style=\"background-color:lightgray;\" >Hello from Python!</h2>" \
           "<h3>AppVersion : 1.0</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "</body>"

    return html.format(hostname=socket.gethostname())

@app.route("/jsonSecret")
def getSecrets():
    jsonOutput = secrets.getJson()
    #response = Flask.Response(jsonOutput)
    #response.headers["Content-Type"] = "application/json"
    #response.headers["App-Version"] = "0.0.1"
    return jsonOutput

@app.route("/getSecret")
def getSingleSecret():
    jsonOutput = secrets.getJson()
    print(request.args)
    if 'id' in request.args:
        id = int(request.args['id'])
        print(id)
    return request.args

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
