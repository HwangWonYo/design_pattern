#-*- encoding: utf-8 -*-
"""
    추상 팩토리 메서드는 관련있는 여러 서브 클래스들을 묶어줄 때 사용할 수 있다.
    앞서 팩토리 메서드에서


    AbstraactFactory 클래스를 사용해서 팩토리의 인터페이스를 정의했기 때문에
    create_protocol, create_port, create_parser 메소드가 여기 포함된다
"""

import abc
import urllib2
from BeautifulSoup import BeautifulStoneSoup


class AbstractFactory(object):
    """추상 팩토리 인터페이스는 서브클래스에서 세 가지 메소드를 제공한다.
    create_protocol, create_port, create_parser"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        """is_secure가 True라면, 팩토리는 보안 연결을 사용한다."""
        self.is_secure = is_secure

    @abc.abstractmethod
    def create_protocol(self):
        pass

    @abc.abstractmethod
    def create_port(self):
        pass

    @abc.abstractmethod
    def create_parser(self):
        pass


class HTTPFactory(AbstractFactory):
    """HTTP 연결을 위한 실제 팩토리"""

    def create_protocol(self):
        if self.is_secure:
            return 'https'
        return 'http'

    def create_port(self):
        if self.is_secure:
            return HTTPSecurePort()
        return HTTPPort()

    def create_parser(self):
        return HTTPParser()


class FTPFactory(AbstractFactory):
    """FTP 연결을 위한 실제 팩토리"""

    def create_protocol(self):
        return 'ftp'

    def create_port(self):
        return FTPPort()

    def create_parser(self):
        return FTPParser()


class Port(object):
    __metaclass__ = abc.ABCMeta
    """연결할 포트를 나타내는 추상 생성물.
    팩토리 메소드에서 이것의 서브클래스를 생성한다."""

    @abc.abstractmethod
    def __str__(self):
        pass


class HTTPPort(Port):
    """http 포트를 나타내는 실제 생성물"""
    def __str__(self):
        return '80'


class HTTPSecurePort(Port):
    """https 포트를 나타내는 실제 생성물"""
    def __str__(self):
        return '443'


class FTPPort(Port):
    """ftp 포트를 나타내는 실제 생성물"""
    def __str__(self):
        return '21'


class Parser(object):
    """
    웹 콘텐츠를 파싱하는 파서를 나타내는 추상 생성물.
    이 것의 서브클래스가 팩토리 메소드에서 생성된다.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, content):
        pass


class HTTPParser(Parser):
    def __call__(self, content):
        filenames = []
        soup = BeautifulStoneSoup(content)
        links = soup.table.findAll('a')
        for link in links:
            filenames.append(link.text)
        return '\n'.join(filenames)


class FTPParser(Parser):
    def __cal__(self, content):
        lines = content.split('\n')
        filenames = []
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])

        return '\n'.join(filenames)


class Connector(object):
    """client"""
    def __init__(self, factory):
        """팩토리는 AbstractFactory 인스턴스로,
        팩토리 클래스에 따라 커넥터의 모든 속성을 생성한다."""
        self.protocol = factory.create_protocol()
        self.port = factory.create_port()
        self.parse = factory.create_parser()

    def read(self, host, path):
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print('Conneting to ', url)
        return urllib2.urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def parse(self):
        pass


if __name__ == "__main__":
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD/'

    protocol = input('Connecting to {}. Which Protocol to use? (0-http, 1-ftp): '.format(domain))

    if protocol == 0:
        is_secure = bool(input('Use secure connection? (1-yes, 0-no): '))
        factory = HTTPFactory(is_secure)
    elif protocol == 1:
        is_secure = False
        factory = FTPFactory(is_secure)
    else:
        print('Sorry, wrong answer')

    connector = Connector(factory)
    try:
        content = connector.read(domain, path)
    except urllib2.URLError, e:
        print('Can not access resource with this method')
    else:
        print(connector.parse(connector))