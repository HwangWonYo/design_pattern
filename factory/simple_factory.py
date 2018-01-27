#-*- encoding: utf-8 -*-
"""
어떤 인스턴스를 생성할 것인가
그 인스턴스를 어떻게 활용할 것이가를 분기할 수 있다.
그렇게 되면 새로운 클래스가 추가된다고 하더라도 코드의 개선 시간을 줄일 수 있다.
클래스를 추가하고 팩토리 메서드에 조건식을 하나 더 추가해서 분기하면 된다.

단 펙토리 메서드가 생성하는 인스턴스들의 인터페이스는 모두 통일되어야 한다.
즉, 같은 동작을 기대할 수 있는 클래스를 분기 생성할 때 사용할 수 있다.
"""

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