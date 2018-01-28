#-*- encoding:utf-8 -*-
"""
    Facade Pattern
    ~~~~~~~~~~~~~~

    장점
    - 클라이언트와 서브시스템의 연결을 느슨하게 만든다.
    - 서브시스템에 접근하는 인터페이스를 제공한다. (수정이 필요 없다)
    - 더 단순한 인터페이스로 복잡한 서브시스템을 감싼다.
    - 서브시스템 구현의 유연성이 높아지고 클라이언트는 더욱 단순해진다.

    복잡한 내부처리 내용을 일괄적으로 처리해준다.
    http://hongjinhyeon.tistory.com/46
    위 블로그에 나와있는 스타크래프 유닛 생성에 대한 예시가 적절하다고 생각한다.
    유닛을 생성하기 위해서는 여러 서브시스템이 작동해야한다.
    가령 탱크를 생성한다고 했을 때
    미네랄 및 가스 여부를 체크하고
    가능한 인구수를 체크하고
    유닛 생성을 시작하고
    미네랄 및 가스를 감소시키고
    인구수를 증가시켜야한다.
    이 서브시스템을 퍼사드 패턴을 사용하여 클라이언트는 Create 메소드 하나로 해결할 수 있다
    추후에 서브시템의 동작을 수정해야 한다면 클라이언트를 수정할 필요 없이
    각각의 수정이 필요한 서브시스템을 수정하면 된다.
"""
import urllib
import urllib2

class WeatherProvider(object):
    def __init__(self):
        self.api_url = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}'

    def get_weather_data(self, city, country):
        city = urllib.quote(city)
        url = self.api_url.format(city, country)
        return urllib2.urlopen(url).read()



from datetime import datetime
import json

class Parser(object):
    def parse_weather_data(self, weather_data):
        parsed = json.loads(weather_data)
        start_date = None
        result = []

        for data in parsed['list']:
            date = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
            start_date = start_date or datetime
            if start_date.day != date.day:
                return result
            result.append(data['main']['temp'])


from datetime import timedelta
import pickle

class Cache(object):
    def __init__(self, filename):
        self.filename = filename

    def save(self, obj):
        with open(self.filename, 'w') as file:
            dct = {
                'obj': obj,
                'expired': datetime.utcnow() + timedelta(hours=3)
            }
            pickle.dump(dct, file)

    def load(self):
        try:
            with open(self.filename) as file:
                result = pickle.load(file)
                if result['expired'] > datetime.utcnow():
                    return result['obj']
        except IOError:
            pass



class Converter(object):
    def from_kelvin_to_cecius(self, kelvin):
        return kelvin - 273.15


class Weather(object):
    def __init__(self, data):
        result = 0

        for r in data:
            result += r

        self.temperature = result / len(data)


class Facade(object):
    def get_forecast(self, city, country):
        cache = Cache('myfile')

        cache_result = cache.load()

        if cache_result:
            return cache_result

        else:
            weather_provider = WeatherProvider()
            weather_data = weather_provider.get_weather_data(city, country)

            parser = Parser()
            parsed_data = parser.parse_weather_data(weather_data)

            weather = Weather(parsed_data)
            converter = Converter()
            temperature_celcius = converter.from_kelvin_to_cecius(weather.temperature)

            cache.save(temperature_celcius)
            return temperature_celcius


if __name__ == "__main__":
    facade = Facade()
    print facade.get_forecast('London', 'UK')