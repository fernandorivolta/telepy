from bin.tools import Tools
class Install():
    def __init__(self):
        self.tools = Tools()

    def install_telegraf(self, sftp, ssh, server):
        sftp.put('/opt/telepy/resources/telegraf-1.12.1-1.x86_64.rpm', '/tmp/telegraf-1.12.1-1.x86_64.rpm')
        ssh.exec_command("rpm -ivh /tmp/telegraf-1.12.1-1.x86_64.rpm > /dev/null 2>&1; sed -i '86s/.*/  hostname=\""+server.hostname+"\"/g' /etc/telegraf/telegraf.conf")
        
    def configure_telegraf(self, ssh, server):
        st = ssh.exec_command('rpm -qa | grep telegraf; sed -n 86p /etc/telegraf/telegraf.conf')[1]
        stdout = st.readlines()
        #verifica se o hostname esta no /etc/telegraf/telegraf.conf na linha 86 e verifica se o "telegraf" esta
        #no rpm -qa | grep telegraf
        if server.hostname in stdout[1] and "telegraf" in stdout[0]:
            server.code="020"
            server.message=self.tools.return_code(server.code)
        else:
            server.code="021"
            server.message=self.tools.return_code(server.code)