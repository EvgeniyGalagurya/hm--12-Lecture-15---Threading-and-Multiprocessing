import json
from urllib.request import urlopen
import threading
from decimal import Decimal

url_nbu = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
url_privat = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'
url_mono = 'https://api.monobank.ua/bank/currency'

course = {}


def make_request(url):
    response = urlopen(url)
    data = response.read()
    data = data.decode('utf-8')
    res = json.loads(data)
    return res


def get_course_privat():
    """Get current temperature from parsed JSON."""
    res = make_request(url_privat)
    current = res[0]
    cur = current['sale']
    course['Privat'] = cur
    return course


def get_course_nbu():
    """Get current temperature from parsed JSON."""
    res = make_request(url_nbu)
    current = res[31]
    cur = current['rate']
    course['NBU'] = cur
    return course


def get_course_mono():
    """Get current temperature from parsed JSON."""
    res = make_request(url_mono)
    current = res[1]
    cur = current['rateSell']
    course['Mono'] = cur
    return course


def get_best_course():
    n = threading.Thread(target=get_course_nbu)
    p = threading.Thread(target=get_course_privat)
    m = threading.Thread(target=get_course_mono)

    n.start()
    p.start()
    m.start()

    n.join()
    p.join()
    m.join()
    # print(course)

    if Decimal(course['Privat']) < Decimal(course['Mono']):
        print('Курс Євро в НБУ на сьогодні складає ' + str(course['NBU']) +
              'грн. за 1 Євро. Найвигідніший курс купівлі Євро в Приватбанку '
              'та складає ' + course['Privat'] + 'грн. за 1 Євро')
    else:
        print('Курс Євро в НБУ на сьогодні складає ' + str(course['NBU']) +
              'грн. за 1 Євро. Найвигідніший курс купівлі Євро в Монобанку '
              'та складає ' + str(course['Mono']) + 'грн. за 1 Євро')


get_best_course()
