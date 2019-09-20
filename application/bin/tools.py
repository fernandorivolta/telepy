import paramiko
class Tools():
    #criacao do objeto ssh (criacao da conexao com servidor), retorna ssh se possivel, 0 com erro e seta o server.code
    #usa o createftp como 0 por padrao, só criando a conexao ftp quando a flag vier 1
    def create_ssh(self, server, createftp = 0):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
            ssh.connect(server.ip, username = 'root', password = server.rootpass, timeout = 1)
            server.code='001'
            server.ssh=True
            if createftp == 1:
                ftp = ssh.open_sftp()
                return ssh, ftp
            return ssh
        except (paramiko.SSHException, IOError) as e:
            #exception de senha invalida
            if isinstance(e, paramiko.AuthenticationException):
                server.code='003'
                server.ssh=False
                return 0
            #qualquer outra exception, na maioria dos casos host indisponivel
            else:
                server.code='002'
                server.ssh=False
                return 0

    def return_code(self, code):
        if (code=='001'):
            return "Conexao estabelecida"
        elif(code=='002'):
            return "Conexao nao estabelecida"
        elif(code=='003'):
            return "Senha invalida"
        elif(code=='010'):
            return "Versao de rhel nao suportada pelo telegraf"
        elif(code=='999'):
            return "OK"