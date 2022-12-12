import pandas as pd

df = pd.read_csv('shops.csv')

# 음식점 데이터만 쓸 겁니다
df = df.loc[df['상권업종대분류명'] == '음식']

# 다음과 같은 칼럼만 있으면 됩니다
df = df[['상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '행정동명', '위도', '경도']]

# 그 중에서도 흑석동과 상도1동만 쓸 겁니다.
df = df.loc[(df['행정동명'] == '상도1동')]

# 칼럼명 단순화

df.columns = ['name',  # 상호명
              'cate_1',  # 중분류명
              'cate_2',  # 소분류명
              'cate_3',  # 표준산업분류명
              'dong',  # 행정동명
              'lon',  # 위도
              'lat'  # 경도
              ]

# path = 'stores.csv'
# df.to_csv(path_or_buf=path, header=True, index=False)

csv_for_clang = df[['name', 'cate_1', 'cate_2']]
path = "ssu_restaurant.csv"
csv_for_clang.to_csv(path_or_buf=path, header=True, index=False)
# print(csv_for_clang)


###### 각 카테고리별 csv를 만들기 위한 부분 ######
kor = csv_for_clang.loc[df['cate_1'] == '한식']
cafe = csv_for_clang.loc[df['cate_1'] == '커피점/카페']
chn = csv_for_clang.loc[df['cate_1'] == '중식']
cake = csv_for_clang.loc[df['cate_1'] == '제과제빵떡케익']
fast = csv_for_clang.loc[df['cate_1'] == '패스트푸드']
jpn = csv_for_clang.loc[df['cate_1'] == '일식/수산물']
alc = csv_for_clang.loc[df['cate_1'] == '유흥주점']
wst = csv_for_clang.loc[df['cate_1'] == '양식']
mil = csv_for_clang.loc[df['cate_1'] == '분식']
fusion = csv_for_clang.loc[df['cate_1'] == '별식/퓨전요리']
chick = csv_for_clang.loc[df['cate_1'] == '닭/오리요리']
etc = csv_for_clang.loc[df['cate_1'] == '기타음식업']

categories = ['kor', 'cafe', 'chn', 'cake', 'fast',
              'jpn', 'alc', 'wst', 'mil', 'fusion', 'chick', 'etc']
data_cate = [kor, cafe, chn, cake, fast,
             jpn, alc, wst, mil, fusion, chick, etc]


# csv 출력
for cate in range(len(categories)):
    path = 'cate/'
    path += (categories[cate] + '.csv')
    data = data_cate[cate]
    data = data[['name']]
    data.to_csv(path_or_buf=path, header=True, index=False)
