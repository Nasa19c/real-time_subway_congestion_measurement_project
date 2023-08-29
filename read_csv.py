import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# Load data from CSV file
data = pd.read_csv('SUBWAY_MONTH.csv', encoding='utf-8')  # 변경: 파일 경로 수정
combined_data = data[data['역명'].isin(['서울역', '종각', '시청'])].copy()

# '시청' 역의 일별 승차총승객수 그래프 그리기 함수
def draw_si_station_chart(data):
    # '시청' 역의 데이터만 추출
    si_data = data[data['역명'] == '시청'].copy()  # .copy() 추가
    # 날짜(datetime) 형식으로 변환
    si_data['사용일자'] = pd.to_datetime(si_data['사용일자'], format='%Y%m%d')
    plt.figure(figsize=(6, 3))
    plt.plot(si_data['사용일자'], si_data['승차총승객수'], marker='o')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/si_station_chart.png')


# '시청' 역의 요일별 승차총승객수 바 차트 그리기 함수
def draw_si_station_weekday_chart(data):
    # '시청' 역의 데이터만 추출
    시청_data = data[data['역명'] == '시청'].copy()  # 복사본 생성
    # 사용일자를 datetime 형식으로 변환
    시청_data.loc[:, '사용일자'] = pd.to_datetime(시청_data['사용일자'], format='%Y%m%d')
    # 사용일자에서 요일을 추출 (0: 월요일, 1: 화요일, ..., 6: 일요일)
    시청_data.loc[:, '요일'] = 시청_data['사용일자'].dt.dayofweek
    # 요일 이름으로 변환
    요일별_이름 = ['월', '화', '수', '목', '금', '토', '일']
    시청_data.loc[:, '요일명'] = 시청_data['요일'].apply(lambda x: 요일별_이름[x])
    # 요일 순서를 월요일부터 일요일까지로 변경
    요일별_이름_변경 = ['월', '화', '수', '목', '금', '토', '일']
    # 요일별 승차총승객수 합계 계산 및 요일 순서대로 정렬
    요일별_승차총승객수 = 시청_data.groupby('요일명')['승차총승객수'].sum().loc[요일별_이름_변경]

    plt.figure(figsize=(6, 3))
    요일별_승차총승객수.plot(kind='bar', color='skyblue')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/si_station_weekday_chart.png')

# '종각'역의 일별승차총승객수 그래프 그리기 함수
def draw_jong_station_chart(data):
    # '종각' 역의 데이터만 추출
    jong_data = data[data['역명'] == '종각'].copy()
    # 날짜(datetime) 형식으로 변환
    jong_data['사용일자'] = pd.to_datetime(jong_data['사용일자'], format='%Y%m%d')
    # 날짜별 승차총승객수에 대한 꺾은선 그래프 그리기
    plt.figure(figsize=(6, 3))
    plt.plot(jong_data['사용일자'], jong_data['승차총승객수'], marker='o')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/jong_station_chart.png')

# '종각' 역의 요일별 승차총승객수 바 차트 그리기 함수
def draw_jong_station_weekday_chart(data):
    # '종각' 역의 데이터만 추출
    종각_data = data[data['역명'] == '종각'].copy()
    # 사용일자를 datetime 형식으로 변환
    종각_data.loc[:, '사용일자'] = pd.to_datetime(종각_data['사용일자'], format='%Y%m%d')
    # 사용일자에서 요일을 추출 (0: 월요일, 1: 화요일, ..., 6: 일요일)
    종각_data.loc[:, '요일'] = 종각_data['사용일자'].dt.dayofweek
    # 요일 이름으로 변환
    요일별_이름 = ['월', '화', '수', '목', '금', '토', '일']
    종각_data.loc[:, '요일명'] = 종각_data['요일'].apply(lambda x: 요일별_이름[x])
    # 요일 순서를 월요일부터 일요일까지로 변경
    요일별_이름_변경 = ['월', '화', '수', '목', '금', '토', '일']
    # 요일별 승차총승객수 합계 계산 및 요일 순서대로 정렬
    요일별_승차총승객수 = 종각_data.groupby('요일명')['승차총승객수'].sum().loc[요일별_이름_변경]

    # 요일별 막대 그래프 그리기
    plt.figure(figsize=(6, 3))
    요일별_승차총승객수.plot(kind='bar', color='skyblue')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/jong_station_weekday_chart.png')

# '서울'역의 일별승차총승객수 그래프 그리기 함수
def draw_se_station_chart(data):
    # '서울' 역의 데이터만 추출
    se_data = data[data['역명'] == '서울역'].copy()
    # 날짜(datetime) 형식으로 변환
    se_data['사용일자'] = pd.to_datetime(se_data['사용일자'], format='%Y%m%d')

    # 날짜별 승차총승객수에 대한 꺾은선 그래프 그리기
    plt.figure(figsize=(6, 3))
    plt.plot(se_data['사용일자'], se_data['승차총승객수'], marker='o')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/se_station_chart.png')

def draw_se_station_weekday_chart(data):
    # '서울' 역의 데이터만 추출
    서울_data = data[data['역명'] == '서울역'].copy()
    # 사용일자를 datetime 형식으로 변환
    서울_data.loc[:, '사용일자'] = pd.to_datetime(서울_data['사용일자'], format='%Y%m%d')
    # 사용일자에서 요일을 추출 (0: 월요일, 1: 화요일, ..., 6: 일요일)
    서울_data.loc[:, '요일'] = 서울_data['사용일자'].dt.dayofweek
    # 요일 이름으로 변환
    요일별_이름 = ['월', '화', '수', '목', '금', '토', '일']
    서울_data.loc[:, '요일명'] = 서울_data['요일'].apply(lambda x: 요일별_이름[x])
    # 요일 순서를 월요일부터 일요일까지로 변경
    요일별_이름_변경 = ['월', '화', '수', '목', '금', '토', '일']
    # 요일별 승차총승객수 합계 계산 및 요일 순서대로 정렬
    요일별_승차총승객수 = 서울_data.groupby('요일명')['승차총승객수'].sum().loc[요일별_이름_변경]

    # 요일별 막대 그래프 그리기
    plt.figure(figsize=(6, 3))
    요일별_승차총승객수.plot(kind='bar', color='skyblue')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/se_station_weekday_chart.png')

def draw_station_chart(data):
    combined_data['사용일자'] = pd.to_datetime(combined_data['사용일자'], format='%Y%m%d')

    # 일별 승차총승객수 합계 계산
    daily_total_passengers = combined_data.groupby('사용일자')['승차총승객수'].sum()

    # 일별 꺾은선 그래프 그리기
    plt.figure(figsize=(6, 3))
    plt.plot(daily_total_passengers.index, daily_total_passengers.values, marker='o')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/all_station_chart.png')

def draw_station_weekday_chart(data):
    combined_data.loc[:,'사용일자'] = pd.to_datetime(combined_data['사용일자'], format='%Y%m%d')
    combined_data.loc[:,'요일'] = combined_data['사용일자'].dt.dayofweek

    # 요일 이름으로 변환
    요일별_이름 = ['월', '화', '수', '목', '금', '토', '일']
    combined_data.loc[:,'요일명'] = combined_data['요일'].apply(lambda x: 요일별_이름[x])

    # 요일별 순서 정의
    요일별_순서 = ['월', '화', '수', '목', '금', '토', '일']

    # 요일별 승차총승객수 합계 계산 및 요일 순서대로 정렬
    요일별_승차총승객수 = combined_data.groupby('요일명')['승차총승객수'].sum().loc[요일별_순서]

    # 요일별 막대 그래프 그리기
    plt.figure(figsize=(6, 3))
    요일별_승차총승객수.plot(kind='bar', color='skyblue')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/all_station_weekday_chart.png')