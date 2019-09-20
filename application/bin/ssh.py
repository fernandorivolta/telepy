import paramiko
class Tools():
    #criacao do objeto ssh (criacao da conexao com servidor), retorna ssh se possivel, 0 com erro e seta o server.code
    def create_ssh(self, server):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
            ssh.connect(server.ip, username = 'root', password = server.rootpass, timeout = 1)
            server.code='001'
            return ssh
        except (paramiko.SSHException, IOError) as e:
            #exception de senha invalida
            if isinstance(e, paramiko.AuthenticationException):
                server.code='003'
                return 0
            #qualquer outra exception, na maioria dos casos host indisponivel
            else:
                server.code='002'
                return 0

    #recebe um objeto server, verifica a versao do rhel
    def verify_rhel_version(self, server):
        if server.ssh != 0:
            rhelversion = server.ssh.exec_command("cat /etc/redhat-release | sed 's/[a-Z]//g' | sed 's/()//g' | xargs")[1].readlines()
            if (float(rhelversion[0].strip('\n')) < 6):
                server.code='010'
                return 0
            else:
                return float(rhelversion[0].strip('\n'))
        else:
            return 0

    def return_code(self, code):
        if (code=='001'):
            return "Conexao estabelecida"
        elif(code=='002'):
            return "Conexao nao estabelecida"
        elif(code=='003'):
            return "Senha inválida"
        elif(code=='010'):
            return "Versao de rhel nao suportada pelo telegraf"
        elif(code=='999'):
            return "OK"