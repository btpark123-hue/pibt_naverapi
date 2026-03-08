# 검색 > 뉴스 - Search API

## 개요

네이버 검색의 뉴스 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 비로그인 방식 오픈 API로, 호출 시 HTTP 헤더에 **Client ID**와 **Client Secret**을 포함해야 합니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 뉴스 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/news.xml`
  - `https://openapi.naver.com/v1/search/news.json`
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 여부 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String (UTF-8) | 필수 | 검색어. 검색어를 UTF-8로 인코딩해야 합니다. |
| `display` | Integer | 선택 | 한 번에 표시할 검색 결과 개수 (기본값: 10, 최댓값: 100) |
| `start` | Integer | 선택 | 검색 시작 위치 (기본값: 1, 최댓값: 1000) |
| `sort` | String | 선택 | 정렬 옵션: `sim` (유사도순, 기본값), `date` (날짜순) |

#### 응답 필드

- `lastBuildDate`: datetime. 검색 결과를 생성한 시간
- `total`: integer. 총 검색 결과 개수
- `start`: integer. 검색 시작 위치
- `display`: integer. 한 번에 표시할 검색 결과 개수
- `items`: 개별 뉴스 검색 결과
  - `title`: string. 뉴스의 제목 (중요 단어는 `<b>` 태그로 강조)
  - `originallink`: string. 제공 언론사의 원본 뉴스 URL
  - `link`: string. 네이버에 연결된 뉴스 URL
  - `description`: string. 뉴스의 요약 내용
  - `pubDate`: string. 뉴스가 보도된 시간 (RFC 822 형식)

## 구현 예제 (Python)

```python
import os
import sys
import urllib.request

clientId = "YOUR_CLIENT_ID"
clientSecret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("주식")
url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",clientId)
request.add_header("X-Naver-Client-Secret",clientSecret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
```

## 오류 코드 가이드

| 상태 코드 | 에러 코드 | 설명 |
| :--- | :--- | :--- |
| 400 | SE01 | 부적절한 query 파라미터 값입니다. |
| 400 | SE02 | 부적절한 display 파라미터 값입니다. |
| 400 | SE03 | 부적절한 start 파라미터 값입니다. |
| 400 | SE04 | 부적절한 sort 파라미터 값입니다. |
| 403 | 403 | API 권한이 없습니다. (API 설정 확인 필요) |
| 500 | 500 | 서버 내부 에러입니다. 부적절한 요청이거나 시스템 장애일 수 있습니다. |

## 주의 사항

- `query`는 반드시 UTF-8로 인코딩되어야 합니다. 그렇지 않으면 한글 검색 시 결과가 나오지 않을 수 있습니다.
- 일 호출 한도는 애플리케이션 등급에 따라 다르며, 기본적으로 일 25,000건(검색 API 전체 합산)입니다.
