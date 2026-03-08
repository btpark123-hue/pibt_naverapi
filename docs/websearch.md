# 검색 > 웹문서 - Search API

## 개요

네이버 검색의 웹 문서(Webkr) 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 네이버의 강력한 웹 수집 엔진이 찾아낸 수천만 건의 웹 페이지 정보를 기반으로 사용자의 질의어에 가장 적합한 웹 문서 리스트를 제공합니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 웹 문서 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/webkr.xml` (XML 응답)
  - `https://openapi.naver.com/v1/search/webkr.json` (JSON 응답)
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET
- **인증**: HTTP 헤더에 Client ID와 Client Secret 포함

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String (UTF-8) | 필수 | 검색어. 검색어는 UTF-8로 인코딩되어야 합니다. |
| `display` | Integer | 선택 | 한 번에 표시할 검색 결과 개수 (기본값: 10, 최댓값: 100) |
| `start` | Integer | 선택 | 검색 시작 위치 (기본값: 1, 최댓값: 1000) |

#### 응답 필드

- `lastBuildDate`: datetime. 검색 결과를 생성한 시간.
- `total`: integer. 검색 결과의 총 개수.
- `start`: integer. 검색 시작 위치.
- `display`: integer. 한 번에 표시할 검색 결과 개수.
- `items`: 검색 결과 항목 리스트.
  - `title`: string. 웹 문서의 제목. (검색어와 일치하는 부분은 `<b>` 태그로 강조됨)
  - `link`: string. 해당 웹 문서의 URL.
  - `description`: string. 웹 문서의 요약 내용.

## 구현 예제 (Python)

```python
import os
import sys
import urllib.request

clientId = "YOUR_CLIENT_ID" # 발급받은 **Client ID**
clientSecret = "YOUR_CLIENT_SECRET" # 발급받은 **Client Secret**

encText = urllib.parse.quote("인공지능")
url = "https://openapi.naver.com/v1/search/webkr.json?query=" + encText # JSON 결과

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

## 응답 예시 (JSON)

```json
{
  "lastBuildDate": "Wed, 28 Sep 2016 16:43:34 +0900",
  "total": 81296956,
  "start": 1,
  "display": 1,
  "items": [
    {
      "title": "네이버 <b>인공지능</b> 기술 개요",
      "link": "https://example.com/ai-tech",
      "description": "네이버에서 연구 중인 다양한 <b>인공지능</b> 기술에 대한 소개와 최신 동향을 제공합니다..."
    }
  ]
}
```

## 오류 코드 가이드 가이드

| 상태 코드 | 상세 사유 | 해결 방안 |
| :--- | :--- | :--- |
| 400 | Invalid parameter | `query` 등 파라미터 이름이나 값이 누락되었는지 확인하세요. |
| 401 | Authentication failed | Client ID/Secret 값이 정확한지 확인하세요. |
| 403 | Forbidden | 애플리케이션 설정에서 '검색' API 사용 신청이 되어 있는지 확인하세요. |
| 429 | Quota exceeded | 일일 호출 한도(25,000건)를 초과했습니다. |
| 500 | Internal server error | 네이버 서버 측 일시적 에러입니다. 잠시 후 재시도하세요. |

## 개발 팁

- **HTML 태그 제거**: `title`과 `description`에 포함된 `<b>` 태그 등은 정규표현식(`String.replace(/<[^>]*>?/gm, '')`) 등을 사용하여 제거 후 화면에 표시하는 것이 좋습니다.
- **검색어 인코딩**: 한글 검색어를 `query` 값으로 넣을 때 반드시 UTF-8 URL 인코딩을 수행해야 결과가 정상적으로 반환됩니다.
- **페이징 처리**: `start`와 `display` 값을 적절히 조합하여 대량의 검색 결과 페이지를 구현할 수 있습니다.
- **캐싱**: 동일한 검색어에 대한 요청이 빈번할 경우 서버 단에서 짧은 시간 동안 결과를 캐싱하여 API 호출 한도를 아낄 수 있습니다.
