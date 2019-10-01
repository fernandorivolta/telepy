from bin.tools import Tools
from influxdb import InfluxDBClient
import time
import paramiko

class Install():
    def __init__(self):
        self.tools = Tools()

    def install_telegraf(self, sftp, ssh, server):
        try:
            sftp.put('/opt/telepy/resources/telegraf-1.12.1-1.x86_64.rpm', '/tmp/telegraf-1.12.1-1.x86_64.rpm')
            ssh.exec_command("rpm -ivh /tmp/telegraf-1.12.1-1.x86_64.rpm > /dev/null 2>&1;")
            sftp.put('/opt/telepy/resources/telegraf.conf', '/etc/telegraf/telegraf.conf')
            ssh.exec_command("sed -i '86s/.*/  hostname=\""+server.hostname+"\"/g' /etc/telegraf/telegraf.conf")
        except paramiko.SSHException as e: 
            print(e)
            server.code='004'
            server.message=self.tools.return_code(server.code)
        
    def configure_telegraf(self, ssh, server):
        st = ssh.exec_command('rpm -qa | grep telegraf; sed -n 86p /etc/telegraf/telegraf.conf')[1]
        ssh.exec_command('service telegraf stop; service telegraf start')
        stdout = st.readlines() 
        #verifica se o hostname esta no /etc/telegraf/telegraf.conf na linha 86 e verifica se o "telegraf" esta
        #no rpm -qa | grep telegraf
        if server.code != '004':
            if len(stdout) > 1:
                if server.hostname in stdout[1] and "telegraf" in stdout[0]:
                    server.code="020"
                    server.message=self.tools.return_code(server.code)
                else:
                    server.code="021"
                    server.message=self.tools.return_code(server.code)
            else:
                server.code="021"
                server.message=self.tools.return_code(server.code)
            
    def validate_grafana_data(self, server):
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('telegraf')
        counter=0
        while(True):
            results = client.query("SHOW series where host='" + server.hostname + "'")
            if (len(results.raw) > 1):
                server.code="030"
                server.message=self.tools.return_code(server.code)
                return 1
            if counter>25:
                server.code="031"
                server.message=self.tools.return_code(server.code)
                return 0
            time.sleep(0.5)
            counter+=1