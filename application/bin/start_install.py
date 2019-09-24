class Install():
    def install_telegraf(self, sftp, ssh, server):
        sftp.put('/opt/telepy/resources/telegraf-1.12.1-1.x86_64.rpm', '/tmp/telegraf-1.12.1-1.x86_64.rpm')
        stdout = ssh.exec_command('rpm -ivh /tmp/telegraf-1.12.1-1.x86_64.rpm;')[1]
        server.code="020"
        server.message="Telegraf instalado"
        