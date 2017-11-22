from cmd import Cmd

from client import FtpClient


class FtpsInterpreter(Cmd):
    """
    FTP command line utility that supports non-secure and secure connections.
    """
    def __init__(self):
        Cmd.__init__(self)
        self.intro = 'FTP(S) Client'
        self.prompt = 'ftp(s) > '
        self._ftp_client = FtpClient()

    def _update_prompt(self):
        prompt = 'ftp(s)'
        if self._ftp_client.host is not None:
            prompt = '{} {}'.format(prompt, self._ftp_client.host)
            if self._ftp_client.user is not None:
                prompt = '{} ({})'.format(prompt, self._ftp_client.user)
        self.prompt = '{} > '.format(prompt)

    def do_connect(self, host):
        """
        Command to connect to an FTP(S) server in the specified host.

        Args:
            host (str): The host to connect to. Defaults to `localhost`.
                        (Optional)
        """
        try:
            response = self._ftp_client.connect(host)
            print response
        except FtpClient.TimeoutException as e:
            print e.msg
        self._update_prompt()

    def do_login(self, *args):
        """
        Command to login with user and password in the connected FTP(S) host.
        """
        user = raw_input('User: ')
        password = raw_input('Password: ')
        try:
            response = self._ftp_client.login(user, password)
            print response
        except FtpClient.TimeoutException as e:
            print e.msg
        except FtpClient.NotConnectedException as e:
            print e.msg
            print('Please connect to an FTP(S) server using the `connect`'
                  ' command.')
        except FtpClient.AuthenticationException as e:
            print e.msg
            print('Failed to authenticate. Please try again.')
        self._update_prompt()

    def do_list(self, filename):
        """
        Command to perform LIST command on the connected FTP(S) host.

        Args:
            filename (str): Name of file or directory to retrieve info
                            for. Defaults to the current directory. (Optional)
        """
        try:
            response = self._ftp_client.list(filename)
            print response
        except FtpClient.TimeoutException as e:
            print e.msg
        except FtpClient.NotConnectedException as e:
            print e.msg
            print('Please connect to an FTP(S) server using the `connect`'
                  ' command.')
        except FtpClient.NotAuthenticatedException as e:
            print e.msg
            print('Please authenticate using the `login` command.')
