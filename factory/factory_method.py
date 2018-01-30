#-*- encoding: utf-8 -*-
"""
    팩토리 메소드
    ~~~~~~~~~

    객체를 생성하기 위한 인터페이스를 정의하는데, 어떤 클래스의 인스턴스를
    만들지는 서브클래스에서 결정하게 만든다. 즉 팩토리 메소드 패턴을 이용하면
    클래스의 인스턴스를 만드는 일을 서브클래스에게 맡기는 것.
    클래스가 독립적으로 관리되기 때문에
    특정 클래스의 변경 사항이 생겼을 때 다른 클래스에 대한 영향을 주지 않는다.

    팩토리 메소드의 장점
    1.  코드를 일반적으로 만들어 실제 클래스에 묶이지 않고 인터페이스의 의존도를 낮춘다.
        인터페이스를 구현으로부터 분리한다. (클라이언트에서 하나의 인터페이스만 사용하면 된다.)
    2.  객체를 생성하는 코드와 사용하는 코드를 분리해서 관리가 쉽도록 한다.
        새로운 클래스를 추가하려면 if-else구문만 추가하면 된다.

    - 인터페이스의 의존도를 낮춘다는 말이 뭘까?
      인터페이스에 의존도가 높다는 것은 하나의 인터페이스에게 많은 일을 위임한다는 뜻이다.
      하나의 인터페이스에서 관리하면 코드가 늘어나 가독성과 효율성 면에서 좋지 못하다.
      인터페이스의 일을 서브클래스에 위임하면 각 서브클래스에서 각각의 기능을 분리해서 관리할 수 있다.
      클라이언트가 할 일은 적절한 서브클래스를 찾는 것 뿐이다.
"""

import abc
import urllib2
from BeautifulSoup import BeautifulStoneSoup

class Connector(object):
    """원격 서버에 연결하기 위한 추상 클래스"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def parse(self, content):
        """
        웹 콘텐츠를 파싱한다.
        이 메소드는 재정의해야만 한다.
        """
        pass

    def read(self, host, path):
        """모든 서브클래스에 대한 일반 메소드로, 웹 콘텐츠를 읽는다."""
        url = self.protocol + "://" + host + ":" + str(self.port) + path
        print 'Connecting to ', url
        return urllib2.urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def protocol_factory_method(self):
        """서브 클래스에서 반드시 재정의해야 하는 팩토리 메소드"""
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        """서브클래스에서 반드시 재정의해야하는 또 다른 팩토리 메소드"""
        pass


class HTTPConnector(Connector):
    """HTTP 커넥터를 생성하고 모든 속성을 runtime에 설정하는 실제 생성자"""
    def protocol_factory_method(self):
        if self.is_secure:
            return 'https'
        return 'http'

    def port_factory_method(self):
        """HTTPPort와 HTTPSecurePort는 실제 객체로, 팩토리 메소드에서 생성한 것이다."""
        if self.is_secure:
            return HTTPSecurePort()
        return HTTPPort()

    def parse(self, content):
        """웹 콘텐츠 파싱"""
        filenames = []
        soup = BeautifulStoneSoup(content)
        links = soup.table.findAll('a')
        for link in links:
            filenames.append(link['href'])
        return '\n'.join(filenames)


class FTPConnector(Connector):
    """FTP 커넥터를 생성하고 모든 속성을 실행 시간에 설정하는 실제 생성자"""
    def protocol_factory_method(self):
        return 'ftp'

    def port_factory_method(self):
        return FTPPort()

    def parse(self, content):
        lines = content.split('\n')
        filenames = []
        for line in lines:
            # 일반적으로 FTP 포맷은 열을 8개 가지고 있다 이것을 나누어 주자
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)


# Interface
class Port(object):
    __metaclass__ = abc.ABCMeta
    """추상 생성물. 이 중 하나의 서브클래스는 팩토리 메소드에서 생성된다."""

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


# Client

if __name__ == "__main__":
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD'

    protocol = input('Connecting to {}. Which Protocol to use? (0-http, 1-ftp): '.format(domain))

    if protocol == 0:
        is_secure = bool(input('Use secure connection? (1-Yes, 0-no): '))
        connector = HTTPConnector(is_secure)
    else:
        is_secure = False
        connector = FTPConnector(is_secure)

    try:
        content = connector.read(domain, path)
    except urllib2.URLError, e:
        print 'Can not access resuorce with this method'
    else:
        print connector.parse(content)