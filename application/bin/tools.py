import paramiko
class Tools():
    #criacao do objeto ssh (criacao da conexao com servidor), retorna ssh se possivel, 0 com erro e seta o server.code
    #usa o createftp como 0 por padrao, só criando a conexao sftp quando a flag vier 1
    def create_ssh(self, server, createsftp = 0):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
            ssh.connect(server.ip, username = 'root', password = server.rootpass, timeout = 1)
            server.code='001'
            server.ssh=True
            if createsftp == 1:
                sftp = ssh.open_sftp()
                return ssh, sftp
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
        elif(code=='011'):
            return "Versao do SO nao compativel com telegraf"
        elif(code=='020'):
            return "Telegraf instalado"
        elif(code=='021'):
            return "Telegraf nao instalado corretamente"
        elif(code=='022'):
            return "Telegraf nao instalado"
        elif(code=='999'):
            return "OK"

    #recebe um objeto server, verifica a versao do rhel
    def verify_rhel_version(self, server, ssh):
        if ssh != 0:
            rhelversion = ssh.exec_command("cat /etc/redhat-release | sed 's/[a-Z]//g' | sed 's/()//g' | xargs")[1].readlines()
            if rhelversion[0].strip('\n') != "":
                if (float(rhelversion[0].strip('\n')) >= 6):
                    return float(rhelversion[0].strip('\n'))
                else:
                    server.code='010'
                    return float(rhelversion[0].strip('\n'))
            else:
                server.code='011'
                server.message=self.return_code(server.code)
                return 0
        else:
            return 0