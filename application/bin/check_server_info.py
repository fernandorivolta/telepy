class CheckServerInfo():
    #recebe um objeto server, verifica a versao do rhel
    def verify_rhel_version(self, server, ssh):
        if ssh != 0:
            rhelversion = ssh.exec_command("cat /etc/redhat-release | sed 's/[a-Z]//g' | sed 's/()//g' | xargs")[1].readlines()
            if (float(rhelversion[0].strip('\n')) < 6):
                server.code='010'
                return 0
            else:
                return float(rhelversion[0].strip('\n'))
        else:
            return 0