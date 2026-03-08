import os
import json
import urllib.request
from datetime import datetime, timedelta
import csv

def load_config():
    # 1. 환경 변수 우선
    client_id = os.environ.get("NAVER_CLIENT_ID")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET")
    if client_id and client_secret:
        return {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

    # 2. 로컬 파일 확인
    config_path = 'api_config.json'
    if not os.path.exists(config_path):
        # 샘플 파일이 있으면 안내
        if os.path.exists('api_config_sample.json'):
            print("Error: API 설정이 없습니다. 환경 변수(NAVER_CLIENT_ID, NAVER_CLIENT_SECRET) 또는 'api_config.json' 파일을 설정해주세요.")
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_search_trend(config):
    url = "https://openapi.naver.com/v1/datalab/search"
    
    # 최근 1년 기간 설정
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "keywordGroups": [
            {
                "groupName": "Gemini",
                "keywords": ["Gemini", "제미나이", "구글 제미나이", "Google Gemini"]
            },
            {
                "groupName": "Claude",
                "keywords": ["Claude", "클로드", "앤스로픽 클로드", "Anthropic Claude"]
            }
        ]
    }
    
    request_body = json.dumps(body, ensure_ascii=False)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", config.get("X-Naver-Client-Id"))
    request.add_header("X-Naver-Client-Secret", config.get("X-Naver-Client-Secret"))
    request.add_header("Content-Type", "application/json")
    
    try:
        response = urllib.request.urlopen(request, data=request_body.encode("utf-8"))
        if response.getcode() == 200:
            return json.loads(response.read().decode('utf-8'))
        else:
            print(f"Error: API 응답 코드가 {response.getcode()}입니다.")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def save_to_csv(data):
    if not data or 'results' not in data:
        print("Error: 저장할 데이터가 없습니다.")
        return

    # data 폴더 생성
    if not os.path.exists('data'):
        os.makedirs('data')
        
    file_path = 'data/ai_trend_data.csv'
    
    # 데이터 구조 재구성 (날짜별로 정렬)
    # results[0] = Gemini, results[1] = Claude
    trends = {} # {date: {Gemini: ratio, Claude: ratio}}
    
    for result in data['results']:
        label = result['title']
        for entry in result['data']:
            period = entry['period']
            ratio = entry['ratio']
            if period not in trends:
                trends[period] = {}
            trends[period][label] = ratio
            
    # CSV 저장
    sorted_dates = sorted(trends.keys())
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Gemini_Ratio', 'Claude_Ratio'])
        for date in sorted_dates:
            gemini = trends[date].get('Gemini', 0)
            claude = trends[date].get('Claude', 0)
            writer.writerow([date, gemini, claude])
            
    print(f"Success: 데이터가 '{file_path}'에 저장되었습니다. (총 {len(sorted_dates)}건)")

def main():
    config = load_config()
    if not config:
        return
        
    print(f"데이터 수집 중: Gemini vs Claude (최근 1년)...")
    result_data = fetch_search_trend(config)
    
    if result_data:
        save_to_csv(result_data)

if __name__ == "__main__":
    main()
