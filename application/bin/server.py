class Server(object):
    def __init__(self):
        self._id = None
        self._ip = None
        self._hostname = None
        self._rootpass = None
        self._ssh = None
        self._code = 999
        self._rhelversion = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def rhelversion(self):
        return self._rhelversion

    @rhelversion.setter
    def rhelversion(self, rhelversion):
        self._rhelversion = rhelversion

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def ssh(self):
        return self._ssh

    @ssh.setter
    def ssh(self, ssh):
        self._ssh = ssh

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        self._ip = ip
    
    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        self._hostname = hostname

    @property
    def rootpass(self):
        return self._rootpass

    @rootpass.setter
    def rootpass(self, rootpass):
        self._rootpass = rootpass

