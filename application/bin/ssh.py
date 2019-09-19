import paramiko
class Tools():
    def create_ssh(self, server):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
            ssh.connect(server.ip, username = 'root', password = server.rootpass, timeout = 1)
            return ssh
        except (paramiko.SSHException, IOError) as se:
            server.message="ERRO - CONEXAO SSH NAO CRIADA"
            return 0

    def verify_rhel_version(self, server):
        rhel_version=6
        if server.ssh!=0:
            rhel_version=7
        return rhel_version
