from flask import Flask, render_template, request, jsonify
from views import views
import requests
import time
import speedtest
import sys, time, io, requests, threading
import subprocess
import re

app = Flask(__name__)
app.register_blueprint(views, url_prefix = "/views")

@app.route('/')
def index():
    return render_template('index.html')

def speed_test(size=5, ipv="ipv4", port=80):
    if size == 1024:
        size = "1GB"
    else:
        size = f"{size}MB"
    url = f"http://{ipv}.download.thinkbroadband.com:{port}/{size}.zip"
    with io.BytesIO() as f:
        start = time.perf_counter()
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        if total_length is None: # no content length header
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                done = int(30 * dl / int(total_length))
                sys.stdout.write("\r[%s%s] %s Mbps" % ('=' * done, ' ' * (30-done), dl//(time.perf_counter() -
start) / 100000))
    print(f"\n{size} = {(time.perf_counter() - start):.2f} seconds")
    t_download_datasize =   f"\n{size}"
    t_download_time = f"\n{(time.perf_counter() - startP):.2f} seconds"
    t_download_speed = dl//(time.perf_counter() - start) / 100000
    return t_download_time,  t_download_speed, t_download_datasize 
 
def measure_ping_speed():
 try:
        output = subprocess.check_output(['ping', 'www.google.com'])
        output = output.decode('utf-8')
        matches = re.search(r'(\d+\.\d+) ms', output)
        if matches:
            ping_speed = float(matches.group(1))
            return ping_speed
 except subprocess.CalledProcessError:
    pass
    return None

   
@app.route('/measure', methods=['POST'])
def measure():
    if request.method == 'POST':
        ########BEGIN CODE
        t_download_time,  t_download_speed, t_download_datasize = speed_test(100, port=8080)#Add new line
        download_datasize = t_download_datasize
        download_datatime = t_download_time
        download_speed = t_download_speed 

        st = speedtest.Speedtest()
        upload_speed = st.upload() / 10**6  # Convert to Mbps
        
        
        #ping_speed = measure_ping_speed()
        #if ping_speed is not None:
        #    print(f"Ping hızı: {ping_speed:.2f} ms")
        #else:
        #    print("Ping hızı ölçülemedi.")
        ping = st.results.ping

        ########END CODE
    return render_template('measure.html',  download_datatime=download_datatime, download_datasize=download_datasize, download_speed=download_speed, upload_speed=upload_speed, ping=ping)

if __name__ == '__main__':
    app.run(debug=True, port=8000,host='0.0.0.0')
