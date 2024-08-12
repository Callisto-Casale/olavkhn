# Imports 
import hashlib
import hmac
from http.client import HTTPException
import os
import subprocess
from flask import Flask, request
from flask import render_template
from dotenv import load_dotenv
load_dotenv()
# Test comment 7

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/test")
def test():
    return 'It automaticlly reloads!'

def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")

@app.route('/reload', methods=['POST'])
def github_reload():
    """

    A function to reload the Flask server when a push event is received from GitHub.
    
    """
    
    payload_body = request.get_data()
    signature_header = request.headers.get('X-Hub-Signature-256')
    try:
        verify_signature(payload_body, os.getenv("GITHUB_TOKEN"), signature_header)
    except Exception as e:
        return str(e), 403

    # Check if the request is from GitHub
    if request.headers.get('X-GitHub-Event') == 'push':
        # Pull the latest changes from the repository
        subprocess.run(['git', 'pull'])
        return 'Webhook received', 200
    else:
        return 'Not a push event', 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=99, debug=True)