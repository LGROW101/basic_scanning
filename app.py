import subprocess
from flask import Flask, request, render_template, jsonify  
import re
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url = request.form['url']
    
    # scan Nmap
    nmap_result = subprocess.run(["nmap", "-sV", url], capture_output=True, text=True)
    nmap_output = nmap_result.stdout
    
    # scan Nikto
    nikto_result = subprocess.run(["nikto", "-h", url], capture_output=True, text=True)
    nikto_output = nikto_result.stdout
    
   
    
    return render_template('result.html', nmap_output=nmap_output, nikto_output=nikto_output)

if __name__ == '__main__':
    app.run(debug=True)
