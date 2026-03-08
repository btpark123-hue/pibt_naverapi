# 검색 > 이미지 - Search API

## 개요

네이버 검색의 이미지 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 고해상도 이미지 정보와 원본 링크를 포함하여 뉴스, 블로그, 웹 등에 포함된 생생한 이미지 자료를 수집할 수 있습니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 이미지 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/image.xml`
  - `https://openapi.naver.com/v1/search/image.json`
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String | Y | 검색어 (UTF-8 인코딩 필수) |
| `display` | Integer | N | 검색 결과 개수 (1~100, 기본 10) |
| `start` | Integer | N | 검색 시작 위치 (1~1000, 기본 1) |
| `sort` | String | N | 정렬 옵션<br>- `sim`: 유사도순 (기본)<br>- `date`: 날짜순 |
| `filter` | String | N | 사이즈 필터<br>- `all`: 모든 이미지 (기본)<br>- `large`: 큰 사이즈<br>- `medium`: 중간 사이즈<br>- `small`: 작은 사이즈 |

#### 응답 필드

- `total`: 총 검색 결과 수
- `items`: 이미지 결과 리스트
  - `title`: 이미지 제목 (파일명 정보 기반)
  - `link`: 원본 이미지 URL (이미지 직접 연결)
  - `thumbnail`: 이미지 섬네일 URL
  - `sizeheight`: 이미지 세로 크기 (픽셀)
  - `sizewidth`: 이미지 가로 크기 (픽셀)

## 구현 예제 (Python)

```python
import os
import sys
import urllib.request

clientId = "YOUR_CLIENT_ID"
clientSecret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("귀여운 고양이")
url = "https://openapi.naver.com/v1/search/image?query=" + encText + "&display=5&filter=large"

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
  <title>Naver Open API - image ::'고양이'</title>
  <link>http://search.naver.com</link>
  <description>Naver Search Result</description>
  <lastBuildDate>Mon, 26 Sep 2016 10:58:23 +0900</lastBuildDate>
  <total>109741</total>
  <start>1</start>
  <display>1</display>
  <item>
    <title>고양이 젤리 발바닥</title>
    <link>http://cfile2.uf.tistory.com/image/...</link>
    <thumbnail>http://tv02.search.naver.net/ugc?...</thumbnail>
    <sizeheight>533</sizeheight>
    <sizewidth>799</sizewidth>
  </item>
</channel>
</rss>
```

## 오류 및 장애 처리

| 상태 코드 | 상세 사유 | 해결 방안 |
| :--- | :--- | :--- |
| 400 | Invalid sort / display | 파라미터 허용 범위를 넘지 않았는지 확인 |
| 401 | Invalid Client ID | 등록한 애플리케이션의 ID와 Secret이 일치하는지 확인 |
| 403 | Forbidden | 검색 API 사용 설정이 안 되어 있거나 호출 한도 초과 |
| 429 | Too Many Requests | 단시간 내 너무 많은 요청 전송 시 발생 |

## 유의 사항

- 검색 결과 이미지 링크(`link`)는 수집 기간에 따라 유효하지 않을 수 있습니다 (삭제된 이미지 등).
- 저작권 이슈가 있는 이미지가 포함될 수 있으므로 상업적 이용 시에는 주의해야 합니다.
- `filter` 속성을 이용해 고해상도 사진만 골라내는 등 목적에 맞는 이미지 수집이 가능합니다.
