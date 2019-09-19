from flask import Flask, render_template, request, redirect, session, flash, url_for
from datetime import datetime
from bin.server import Server
from bin.ssh import Tools
tools = Tools()

app = Flask(__name__, template_folder='html/')
@app.route('/')
def index():
    return render_template('index.html', last_updated=datetime.now(tz=None))

@app.route('/run',methods = ['POST'])
def run():
    name_test = request.json['teste_name']
    hostList = request.json['servers']
    serverList = []
    for host in hostList:
        server = Server()
        server.hostname = host['hostname']+"_"+name_test
        server.ip = host['ip']
        server.rootpass = host['passwd']
        server.ssh = tools.create_ssh(server)
        server.rhelversion = tools.verify_rhel_version(server)
        serverList.append(server)
    
    for server in serverList:
        print(server.rhelversion)
    return "oi"

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.run(host='0.0.0.0', debug=True) 