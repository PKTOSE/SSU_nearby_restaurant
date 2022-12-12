import getWeather
import pandas as pd
import datetime
import random

now = datetime.datetime.now()

df = pd.read_csv('ssu_restaurant.csv')
weather_data = getWeather.get_naver_weather()  # 맑음, 흐림, 구름 많음, 흐리고 비/눈, 흐리고 눈, 흐리고 비, 비, 눈,
status = weather_data["status"]

# 운량
cloudy = ["한식", "고기"]
sunny = ["한식", "양식", "고기", "구이류", "일식", "중식", "세계음식"]

now_cloud = cloudy  # default cloud
if status == "흐림":
    now_cloud = cloudy
elif status == "맑음":
    now_cloud = sunny

# 계절
spring = ["한식", "갈비", "고기", "구이", "불고기"]
summer = ["삼계탕", "아이스크림", "냉면"]
fall = ["호프", "브런치"]
winter = ["빠", "해물"]

season = winter  # default season
# 파이썬은 &&기호로 연결할 필요 없이 두 개의 범위 구분을 한 번에 쓸 수 있다.
if 3 <= now.month <= 5:
    season = spring

if 6 <= now.month <= 8:
    season = summer

if 9 <= now.month <= 11:
    season = fall

if now.month <= 2 or now.month == 12:
    season = winter


def make_list():
    search_List = []
    for i in range(len(df)):
        for kw in now_cloud:  # 운량에 따른 분류
            if (kw in df.loc[i]['name']) or (kw in df.loc[i]['cate_1']) or (kw in df.loc[i]['cate_2']):
                search_List.append(df.loc[i]['name'])

        for kw in season:  # 계절에 따른 분류
            if (kw in df.loc[i]['name']) or (kw in df.loc[i]['cate_1']) or (kw in df.loc[i]['cate_2']):
                search_List.append(df.loc[i]['name'])

    search_List = list(sorted(search_List))
    # print(search_List)
    return search_List


def get_rdm_from_list():
    search_list = make_list()
    length = len(search_list)
    rdm_idx = random.randint(0, length)
    return search_list[rdm_idx]


if __name__ == "__main__":
    print(get_rdm_from_list())
