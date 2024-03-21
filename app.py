import subprocess
from flask import Flask, request, render_template, redirect, url_for
import re

app = Flask(__name__)

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url = request.form.get('url', '')
    scan_type = request.form.get('scan_type', '')
    
    # ตรวจสอบว่า URL ไม่ว่างเปล่าหรือไม่
    if not url:
        return redirect(url_for('index', error="Invalid URL format"))
    
    # ตรวจสอบรูปแบบของ IP Address
    ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    if not ip_pattern.match(url):
        return redirect(url_for('index', error="Invalid IP Address format"))
  
    try:
        if scan_type == 'quick':
            nmap_result = subprocess.run(["nmap", "-sV", url], capture_output=True, text=True)
        elif scan_type == 'full':
            nmap_result = subprocess.run(["nmap", "-sV", "-p-", "-A", url], capture_output=True, text=True)
        else:
            return redirect(url_for('index', error="Invalid scan type"))

        nmap_output = nmap_result.stdout

        if nmap_result.returncode != 0:
            return redirect(url_for('index', error="Nmap scan failed"))
        else:
            # scan Nikto
            nikto_result = subprocess.run(["nikto", "-h", url], capture_output=True, text=True)
            nikto_output = nikto_result.stdout

            return render_template('result.html', nmap_output=nmap_output, nikto_output=nikto_output, success_message="Scan successful")

    except Exception as e:
        return redirect(url_for('index', error="An error occurred: {}".format(str(e))))

if __name__ == '__main__':
    app.run(debug=True)
