from flask import Flask
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
    jsonOutput = secrets.getSecret()

    return jsonOutput

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
