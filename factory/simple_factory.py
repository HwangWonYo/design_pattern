class SimpleFactory(object):
    @staticmethod
    def build_connection(protocol):
        if protocol == 'http':
            return HTTPConnection()
        elif protocol == 'ftp':
            return FTPConnection()
        else:
            raise RuntimeError('Unknown protocol')


if __name__ == "__main__":
    protocol = input('Which Protocol to use? (http or ftp): ')
    protocol = SimpleFactory.build_connection(protocol)
    protocol.connection()
    print(protocol.get_response())