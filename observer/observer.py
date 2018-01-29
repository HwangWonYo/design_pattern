#-*- encoding:utf-8 -*-
"""
    옵저버 패턴
    ~~~~~~~~

    장점:
        - subject와 observer의 연결이 느슨하도록 유지한다.
          subject는 오직 observer의 리스트만 알고 있고,
          실제 클래스나 자세한 구현 등에 대해선 관심을 갖지 않는다.
        - subject와 observer 간에 메시지 브로드캐스팅을 할 수 있다.
        - observer의 수를 실행 시간에 바꿀 수 있다.
        - subject는 어떠한 수의 observer도 가질 수 있다.
"""

import time

class Subject(object):
    def __init__(self):
        self.observers = []
        self.cur_time = None

    def register_observer(self, observer):
        if observer in self.observers:
            print(observer, 'already in subscribed observers')
        else:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print('No such observer in subject')

    def notify_observers(self):
        self.cur_time = time.time()
        for observer in self.observers:
            observer.notify(self.cur_time)



from abc import ABCMeta, abstractmethod
import datetime

class Observer(object):
    """
    옵저버에 대한 추상 클래스
    notify만을 가지고 있다.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, unix_timestamp):
        pass


class USATimeObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, unix_timpestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timpestamp)).strftime('%Y-%m-%d %I:%M:%S%p')
        print('Observer', self.name, 'says:', time)


class EUTimeObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        print('Observer', self.name, 'says', time)


if __name__ == "__main__":
    subject = Subject()

    print('Adding usa_time_observer')
    observer1 = USATimeObserver('usa_time_observer')
    subject.register_observer(observer1)
    subject.notify_observers()

    time.sleep(2)
    print('Adding eu_time_observer')
    observer2 = EUTimeObserver('eu_time_observer')
    subject.register_observer(observer2)
    subject.register_observer(observer2)
    subject.notify_observers()

    time.sleep(2)
    print('Removing usa_time_observer')
    subject.unregister_observer(observer1)
    subject.notify_observers()
