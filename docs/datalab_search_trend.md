# 통합 검색어 트렌드 - Naver DataLab API

## 개요

네이버 통합검색에서 특정 주제어와 그에 속하는 검색어들의 검색 추이 데이터를 제공하는 RESTful API입니다. 설정한 기간 내의 검색량 변화를 가장 많이 검색된 시점(100)을 기준으로 상대적인 수치(0~100)로 변환하여 JSON 형식으로 반환합니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)

## API 레퍼런스

### 네이버 통합 검색어 트렌드 조회

사용자가 정의한 주제어와 검색어 리스트를 기반으로 검색 추이를 조회합니다.

- **요청 URL**: `https://openapi.naver.com/v1/datalab/search`
- **프로토콜**: HTTPS
- **HTTP 메서드**: POST
- **인증 방식**: HTTP Header (X-Naver-Client-Id, X-Naver-Client-Secret)

#### 요청 파라미터 (JSON Body)

| 필드명 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `startDate` | String | Y | 조회 시작 날짜 (format: `yyyy-mm-dd`) |
| `endDate` | String | Y | 조회 종료 날짜 (format: `yyyy-mm-dd`) |
| `timeUnit` | String | Y | 구간 단위 (`date`, `week`, `month`) |
| `keywordGroups` | Array | Y | 주제어 그룹 설정 (최대 5개 주제어 설정 가능) |
| - `groupName` | String | Y | 주제어 명칭 |
| - `keywords` | Array | Y | 해당 주제어에 포함될 검색어 리스트 (최대 20개) |
| `device` | String | N | 기기 필터 (`pc`, `mo`) |
| `gender` | String | N | 성별 필터 (`m`, `f`) |
| `ages` | Array | N | 연령대 필터 (`1`~`11`) |

#### 연령대 코드표

- `1`: 0~12세, `2`: 13~18세, `3`: 19~24세, `4`: 25~29세, `5`: 30~34세, `6`: 35~39세, `7`: 40~44세, `8`: 45~49세, `9`: 50~54세, `10`: 55~59세, `11`: 60세 이상

## 응답 필드

| 필드명 | 타입 | 설명 |
| :--- | :--- | :--- |
| `startDate` | String | 조회 시작 날짜 |
| `endDate` | String | 조회 종료 날짜 |
| `timeUnit` | String | 구간 단위 |
| `results` | Array | 각 주제어 그룹별 데이터 |
| - `title` | String | 주제어 명칭 |
| - `keywords` | Array | 설정된 검색어 리스트 |
| - `data` | Array | 구간별 검색 상대 수치 데이터 |
| -- `period` | String | 해당 구간의 시작 날짜 |
| -- `ratio` | Double | 해당 구간의 검색 상대 수치 |

## 구현 예제 (Python)

```python
import os
import sys
import urllib.request
import json

clientId = "YOUR_CLIENT_ID"
clientSecret = "YOUR_CLIENT_SECRET"
url = "https://openapi.naver.com/v1/datalab/search"

body = {
    "startDate": "2023-01-01",
    "endDate": "2023-12-31",
    "timeUnit": "month",
    "keywordGroups": [
        {
            "groupName": "인공지능",
            "keywords": ["AI", "인공지능", "ChatGPT"]
        },
        {
            "groupName": "데이터분석",
            "keywords": ["데이터분석", "빅데이터"]
        }
    ],
    "device": "pc",
    "ages": ["3", "4", "5"],
    "gender": "f"
}

request_body = json.dumps(body, ensure_ascii=False)
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", clientId)
request.add_header("X-Naver-Client-Secret", clientSecret)
request.add_header("Content-Type", "application/json")

try:
    response = urllib.request.urlopen(request, data=request_body.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + str(rescode))
except Exception as e:
    print(e)
```

## 오류 코드 가이드 가이드

| 상태 코드 | 에러 메시지 | 해결 방법 |
| :--- | :--- | :--- |
| 400 | Invalid JSON format | 요청 Body의 JSON 형식이 올바른지 확인 |
| 401 | Authentication failed | Client ID/Secret 값이 정확한지 확인 |
| 403 | Forbidden | 애플리케이션 설정에서 '데이터랩' API 권한이 활성화되었는지 확인 |
| 429 | Quota Exceeded | 일일 호출 한도(1,000회)를 초과함 |
| 500 | Internal Server Error | 네이버 시스템 측 장애. 잠시 후 재시도 |

## 활용 팁

- **상대 수치의 이해**: 결과값의 `ratio`는 최대 검색량을 100으로 잡았을 때의 비율입니다. 절대적인 검색 건수가 아님을 유의하세요.
- **날짜 포맷**: 반드시 `yyyy-mm-dd` 형식을 지켜야 하며, 과거 데이터 조회 한도는 서비스 정책에 따릅니다.
- **다양한 필터**: 연령대와 성별 필터를 조합하여 타겟별 트렌드 분석이 가능합니다.
