# 검색 > 지식iN - Search API

## 개요

네이버 검색의 지식iN 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 질문과 답변 데이터를 활용하여 다양한 정보 서비스를 구축할 수 있습니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 지식iN 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/kin.xml`
  - `https://openapi.naver.com/v1/search/kin.json`
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String | Y | 검색어 (UTF-8 인코딩) |
| `display` | Integer | N | 검색 결과 개수 (1~100, 기본 10) |
| `start` | Integer | N | 검색 시작 위치 (1~1000, 기본 1) |
| `sort` | String | N | 정렬 옵션<br>- `sim`: 유사도순 (기본값)<br>- `date`: 날짜순<br>- `point`: 추천순 |

#### 응답 필드

| 필드명 | 설명 |
| :--- | :--- |
| `lastBuildDate` | 검색 결과 생성 시간 |
| `total` | 총 검색 결과 수 |
| `items` | 검색 결과 항목 리스트 |
| - `title` | 지식iN 질문 제목 |
| - `link` | 지식iN 질문 상세 페이지 URL |
| - `description` | 질문 내용 요약 |

## 구현 예제 (Python)

```python
import os
import sys
import urllib.request

clientId = "YOUR_CLIENT_ID"
clientSecret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("주식계좌")
url = "https://openapi.naver.com/v1/search/kin?query=" + encText

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

## 응답 예시 (XML)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Naver Open API - kin ::'주식'</title>
    <link>http://search.naver.com</link>
    <description>Naver Search Result</description>
    <lastBuildDate>Mon, 26 Sep 2016 10:59:15 +0900</lastBuildDate>
    <total>585431</total>
    <start>1</start>
    <display>10</display>
    <item>
      <title>&lt;b&gt;주식&lt;/b&gt;계좌 만드는 방법</title>
      <link>http://openapi.naver.com/l?AAAB2O...</link>
      <description>안녕하세여 제가 &lt;b&gt;주식&lt;/b&gt;계좌를 만들어야 하는데...</description>
    </item>
  </channel>
</rss>
```

## 주요 오류 코드

| 코드 | 설명 |
| :--- | :--- |
| 400 | 잘못된 파라미터 (Query missing 등) |
| 401 | 인증 실패 (ID/Secret 확인) |
| 403 | API 권한 없음 (애플리케이션 설정에서 신청 여부 확인) |
| 429 | 호출 한도 초과 (일 25,000건 초과) |
| 500 | 서버 장애 |

## 활용 가이드

- 질문 제목(`title`)과 내용(`description`)에 포함된 키워드는 `<b>...</b>` 태그로 감싸져 나옵니다. 필요에 따라 정규식을 사용하여 태그를 제거할 수 있습니다.
- 추천순(`point`) 정렬을 활용하면 양질의 답변이 달려 있는 질문을 우선적으로 수집할 수 있습니다.
- `start` 값을 이용해 페이징 처리를 하여 대량의 데이터를 순차적으로 수집할 수 있습니다.
