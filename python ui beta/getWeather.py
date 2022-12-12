from bs4 import BeautifulSoup
from pprint import pprint
import requests


def get_naver_weather():
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    # pprint(html.text)

    soup = BeautifulSoup(html.text, 'html.parser')

    data1 = soup.find('section', {'class': 'sc_new cs_weather_new _cs_weather'})

    # pprint(data1)

    differ_yesterday = data1.find('p', {'class': 'summary'})
    # print(differ_yesterday.text) # "어제보다 4.5° 높아요  흐림 "
    differ_yesterday = differ_yesterday.text
    differ = differ_yesterday[5:9]
    which = differ_yesterday[10:13]
    status = differ_yesterday[-3:].strip()

    # print(f"differ : {differ} | which : {which} | status : {status}")

    now_weather = data1.find('div', {'class': 'temperature_text'})
    # print(now_weather.text) # " 현재 온도2.3°"
    now_weather = now_weather.text[6:-1]
    # print(now_weather)
    datas = {"now_degree": now_weather, "differ": differ, "which": which, "status": status}
    return datas


if __name__ == "__main__":
    print(get_naver_weather())
