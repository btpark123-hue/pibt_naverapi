# 검색 > 오타변환 - Search API

## 개요

사용자가 한/영 키를 잘못 설정하고 입력한 검색어를 올바르게 변환한 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 예를 들어 'spdlqj'를 입력하면 '네이버'로 변환된 결과를 제공합니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 오타 변환 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/errata.xml`
  - `https://openapi.naver.com/v1/search/errata.json`
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String | Y | 변환할 검색어 (UTF-8 인코딩) |

#### 응답 필드

| 필드명 | 타입 | 설명 |
| :--- | :--- | :--- |
| `errata` | string | 오타가 교정된 결과 단어. (교정이 불가능하거나 오타가 아니면 빈 문자열이 올 수 있음) |

## 응답 예시 (JSON)

```json
{
  "result": {
    "item": [
      {
        "errata": "네이버"
      }
    ]
  }
}
```

## 구현 예제 (Python)

```python
import os
import sys
import urllib.request

clientId = "YOUR_CLIENT_ID"
clientSecret = "YOUR_CLIENT_SECRET"
# 'spdlqj'는 한글 모드에서 '네이버'를 영문 모드로 친 오타입니다.
encText = urllib.parse.quote("spdlqj")
url = "https://openapi.naver.com/v1/search/errata?query=" + encText

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

## 주요 오류 코드

| 상태 코드 | 에러 메시지 | 해결 방법 |
| :--- | :--- | :--- |
| 400 | Query missing | query 변수가 요청에 포함되었는지 확인 |
| 401 | Invalid Client ID | 클라이언트 ID가 유효한지 확인 |
| 403 | Forbidden access | 애플리케이션의 검색 API 사용 허가 여부 확인 |
| 500 | System error | 네이버 내부 장애 상태 |

## 개발 팁

- 검색 서비스 구축 시, 사용자가 오타를 입력했을 때 검색창 하단에 "혹시 **{errata}**를 검색하시겠습니까?" 와 같은 추천 메시지를 띄우는 용도로 활용도가 높습니다.
- 자동 완성 기능과 연동하여 사용하면 더욱 강력한 검색 보정 기능을 구현할 수 있습니다.
- 오타 변환 API는 한글 -> 영문, 영문 -> 한글 오타를 모두 판별하여 교정해줍니다.
- 응답값이 있는 경우에만 처리하도록 로직을 구현하는 것이 좋습니다.
