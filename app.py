from flask import Flask, request
import secrets as secrets
import json
import os
import socket

app = Flask(__name__)

port = int(os.environ.get('PORT', 5000))

def selectKeyvault():
    keyvault = ""
    if 'project' not in request.json or 'env' not in request.json:
        abort(400)
    else:
        keyvault = request.json['project']+request.json['env']
        
    return keyvault

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
    keyvault = selectKeyvault()
    jsonOutput = secrets.getJson(keyvault)
    #response = Flask.Response(jsonOutput)
    #response.headers["Content-Type"] = "application/json"
    #response.headers["App-Version"] = "0.0.1"
    return jsonOutput

@app.route("/getSecret")
def getSingleSecret():
    keyvault = selectKeyvault()
    jsonOutput = secrets.getJson(keyvault)
    if "testhpest" in jsonOutput:
        return "This is a test response for testhpest keyvault"
    print(request.args)
    resource = request.args['resource']
    if 'resource' in request.args:
        dictOutput = json.loads(jsonOutput)
        if resource in dictOutput:
            singleSecret = dictOutput[resource]
        else:
            singleSecret = "Resource does not exist"
    else:
        singleSecret = "No resource given"
        
    return singleSecret

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
