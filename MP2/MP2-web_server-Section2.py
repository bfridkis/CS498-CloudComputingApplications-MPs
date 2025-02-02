import os
import getpass
import socket
import subprocess
from flask import Flask, redirect, url_for, request
from subprocess import Popen, PIPE
app = Flask(__name__)

#return_val = "0"

@app.route('/', methods=['POST', 'GET'])
def field_request():
    #global return_val
    if request.method == 'POST':
        try:
            process = subprocess.Popen(['python3', 'stress_cpu.py'])
            return f"Successfully launched stress_cpu.py. PID: {process.pid}"
        except:
            print("Could not launch stress_cpu.py!")
            return "Failure: Could not launch stress_cpu.py."

    elif request.method == 'GET':
        return socket.gethostname()

if __name__ == '__main__':
   app.run(debug = True)
   
# References
# https://github.com/yeshwanthlm/YouTube/blob/main/flask-on-aws-ec2.md
# https://www.youtube.com/watch?v=ct1GbTvgVNM
# https://stackoverflow.com/questions/17413526/nginx-missing-sites-available-directory
# https://stackoverflow.com/questions/52076148/how-to-find-gunicorn-path-in-ubuntu-using-terminal
# https://stackoverflow.com/questions/17413526/nginx-missing-sites-available-directory
# https://www.youtube.com/watch?v=KWIIPKbdxD0
# https://stackoverflow.com/questions/51658198/nginx-emerg-upstream-directive-is-not-allowed-here-in-etc-nginx-sites-enab
# https://www.tutorialspoint.com/flask/flask_http_methods.htm
# https://dev.to/askyt/create-a-file-if-not-exists-in-python-19j3
# https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.5
# https://unix.stackexchange.com/questions/106561/finding-the-pid-of-the-process-using-a-specific-port
# https://www.youtube.com/watch?v=8DbUU83I3zs
# https://stackoverflow.com/questions/7152340/using-a-python-subprocess-call-to-invoke-a-python-script