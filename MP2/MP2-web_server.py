import os
import getpass
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def field_request():
    #print(os.getcwd())
    #print("Env thinks the user is [%s]" % (os.getlogin()))
    #print("Effective user is [%s]" % (getpass.getuser()))
    print(f"Printing request.form:  {request.form}")
    #print(bool(request.form.to_dict()))
    if request.method == 'POST':
        try:
            with open('/home/ec2-user/MP2/seed.txt', 'w') as file:
                if "num" in request.form.to_dict():
                    file.write(request.form['num'])
                    return "Seed value updated with value of request.form['num']"
                else:
                    file.write("0")
                    return "Seed value updated with default value of 0"
        except:
            print("Error opening or creating seed.txt file")
    elif request.method == 'GET':
        try:
            with open('/home/ec2-user/MP2/seed.txt', 'r') as file:
                return file.read()
        except:
            with open('/home/ec2-user/MP2/seed.txt', 'w') as file:
                file.write("0")
                return "0"

if __name__ == '__main__':
   app.run(debug = True)

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