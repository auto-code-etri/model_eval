import requests
import pandas as pd

def get_first_archive_timestamp(url):
    cdx_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": url,
        "fl": "timestamp",
        "limit": 1,
        "output": "json"
    }

    response = requests.get(cdx_url, params=params)

    data = response.json()
    if len(data) > 1:
        # 시간 부분 제거하기
        return data[1][0][:8]
    else:
        return None

# CSV 파일 읽기
df = pd.read_csv('leetcode_dataset.csv')

# 'title' 컬럼의 처음 100줄을 불러오기, 소문자로 바꾸고 띄어쓰기를 '-'로 바꾸기
title_list = df['title'].iloc[:100].str.lower().str.replace(' ', '-').tolist()

# 각 제목에 대한 URL의 첫 아카이브 날짜를 저장할 딕셔너리
first_archive_dates = {}

# 각 제목에 대해
for title in title_list:
    # URL 만들기
    url = f"https://leetcode.com/problems/{title}/"
    
    # 첫 아카이브 날짜 얻기
    first_archive_date = get_first_archive_timestamp(url)

    # 딕셔너리에 저장
    first_archive_dates[title] = first_archive_date

# 딕셔너리 출력해서 확인
for title, date in first_archive_dates.items():
    print(f"{title}: {date}")


# csv 파일에 archive 날짜 추가
import requests
import pandas as pd
import json

def get_first_archive_timestamp(url):
    cdx_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": url,
        "fl": "timestamp",
        "limit": 1,
        "output": "json"
    }

    response = requests.get(cdx_url, params=params)

    data = response.json()
    if len(data) > 1:
        # 시간 부분 제거하기
        return data[1][0][:8]
    else:
        return None

# CSV 파일 읽기
df = pd.read_csv('leetcode_dataset.csv')

# 'title' 컬럼의 처음 100줄을 불러오기, 소문자로 바꾸고 띄어쓰기를 '-'로 바꾸기
title_list = df['title'].iloc[:100].str.lower().str.replace(' ', '-').tolist()

# 각 제목에 대한 URL의 첫 아카이브 날짜를 저장할 딕셔너리
first_archive_dates = {}

# 각 제목에 대해
for title in title_list:
    # URL 만들기
    url = f"https://leetcode.com/problems/{title}/"
    
    # 첫 아카이브 날짜 얻기
    first_archive_date = get_first_archive_timestamp(url)

    # 딕셔너리에 저장
    first_archive_dates[title] = first_archive_date

# 'archive_date' 열을 추가하여 CSV 파일에 저장
df['archive_date'] = df['title'].str.lower().str.replace(' ', '-').map(first_archive_dates)
df.to_csv('leetcode_dataset_with_archive.csv', index=False)


# submit result.json 파일에 archive 날짜 추가
import requests
import pandas as pd
import json

def get_first_archive_timestamp(url):
    cdx_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": url,
        "fl": "timestamp",
        "limit": 1,
        "output": "json"
    }

    response = requests.get(cdx_url, params=params)

    data = response.json()
    if len(data) > 1:
        # 시간 부분 제거하기
        return data[1][0][:8]
    else:
        return None

# CSV 파일 읽기
df = pd.read_csv('leetcode_dataset.csv')

# 'title' 컬럼의 처음 100줄을 불러오기, 소문자로 바꾸고 띄어쓰기를 '-'로 바꾸기
title_list = df['title'].iloc[:100].str.lower().str.replace(' ', '-').tolist()

# 각 제목에 대한 URL의 첫 아카이브 날짜를 저장할 딕셔너리
first_archive_dates = {}

# 각 제목에 대해
for title in title_list:
    # URL 만들기
    url = f"https://leetcode.com/problems/{title}/"
    
    # 첫 아카이브 날짜 얻기
    first_archive_date = get_first_archive_timestamp(url)

    # 딕셔너리에 저장
    first_archive_dates[title] = first_archive_date

# JSON 파일 읽기
with open('compile_result.json', 'r') as f:
    json_data = json.load(f)

# 날짜 정보 추가
for problem in json_data:
    if problem['title'].lower().replace(' ', '-') in first_archive_dates:
        problem['archive_date'] = first_archive_dates[problem['title'].lower().replace(' ', '-')]

# JSON 파일에 다시 쓰기
with open('compile_result.json', 'w') as f:
    json.dump(json_data, f, indent=4)
