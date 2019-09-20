from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from datetime import datetime
from bin.Server import Server
from bin.tools import Tools
from bin.check_server_info import CheckServerInfo
import jsonpickle

check=CheckServerInfo()
tools = Tools()

app = Flask(__name__, template_folder='html/')
@app.route('/')
def index():
    return render_template('index.html', last_updated=datetime.now(tz=None))

@app.route('/check_server_info', methods = ['POST'])
def check_server_info():
    response = []
    servers = []
    name_test = request.json['teste_name']
    hostList = request.json['servers']
    serverList = []
    for host in hostList:
        server = Server()
        server.hostname = host['hostname']+"_"+name_test
        server.ip = host['ip']
        server.rootpass = host['passwd']
        server.rhelversion = check.verify_rhel_version(server, tools.create_ssh(server))
        server.message = tools.return_code(server.code)
        serverList.append(server)
        servers.append(server)

    #envia o json transformando os objetos em python para objetos json
    return jsonify(jsonpickle.encode(servers))

@app.route('/start_install', methods = ['POST'])
def start_install():
    #recebe o json e transforma em objetos python
    servers = jsonpickle.decode(request.json)
    for server in servers:
        #se o ssh ja foi criado antes e a flag esta True
        if server.ssh:
            #com a flag 1 retorna o ftp junto
            ssh, ftp = tools.create_ssh(server, 1)
                

    return jsonify(jsonpickle.encode(servers))

app.run(host='0.0.0.0', debug=True) 