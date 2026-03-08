# 검색 > 쇼핑 - Search API

## 개요

네이버 검색의 쇼핑 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 네이버 쇼핑에 등록된 방대한 상품 정보를 기반으로 가격 비교, 상품 검색 기능을 구현할 수 있습니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 쇼핑 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/shop.xml`
  - `https://openapi.naver.com/v1/search/shop.json`
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String | Y | 검색어. UTF-8 인코딩 필수. |
| `display` | Integer | N | 한 번에 표시할 결과 수 (1~100, 기본 10) |
| `start` | Integer | N | 검색 시작 위치 (1~1000, 기본 1) |
| `sort` | String | N | 정렬 옵션<br>- `sim`: 유사도순 (기본값)<br>- `date`: 날짜순<br>- `asc`: 가격 오름차순<br>- `dsc`: 가격 내림차순 |
| `exclude` | String | N | 제외 옵션. `:`로 구분 (예: `exclude=used:cbshop`) |

#### 응답 필드

- `total`: 총 검색 결과 개수
- `items`: 개별 상품 결과 항목
  - `title`: 상품명 (HTML 태그 포함)
  - `link`: 네이버 쇼핑 상품 상세 페이지 URL
  - `image`: 상품 썸네일 경로
  - `lprice`: 최저가 (숫자 문자열)
  - `hprice`: 최고가 (제공 안 되는 경우 0)
  - `mallName`: 판매처 이름
  - `productId`: 상품 ID
  - `productType`: 상품군 타입 (1: 일반상품, 2: 중고상품 등)
  - `brand`: 브랜드명
  - `maker`: 제조사명

## 구현 예제 (Python)

```python
import os
import sys
import urllib.request

clientId = "YOUR_CLIENT_ID"
clientSecret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("노트북")
url = "https://openapi.naver.com/v1/search/shop?query=" + encText + "&display=10&sort=asc"

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
  "lastBuildDate": "Tue, 04 Oct 2016 13:23:58 +0900",
  "total": 17161390,
  "start": 1,
  "display": 1,
  "items": [
    {
      "title": "허니트립 보스턴백",
      "link": "http://openapi.naver.com/l?AAAB...",
      "image": "http://shopping.phinf.naver.net/main...",
      "lprice": "6700",
      "hprice": "0",
      "mallName": "허니트립",
      "productId": "10315467179",
      "productType": "2",
      "brand": "",
      "maker": "허니트립",
      "category1": "패션잡화",
      "category2": "여행용가방/소품",
      "category3": "보스턴백"
    }
  ]
}
```

## 오류 코드 가이드 요약

| 코드 | 설명 |
| :--- | :--- |
| 400 | 잘못된 파라미터 형식 |
| 401 | 클라이언트 인증 실패 |
| 403 | 권한 부족 (애플리케이션 설정 확인 요망) |
| 429 | 일일 허용량 초과 |
| 500 | 네이버 API 서버 오류 |

## 개발 참고 사항

- `productType`을 활용해 중고상품을 걸러내거나, `sort`를 활용해 최저가 검색 엔진을 구축할 수 있습니다.
- 가격 정보는 문자열 형식이므로 연산 시 형 변환이 필요합니다.
- `mallName`은 복합 판매처일 경우 '네이버' 혹은 특정 오픈마켓 이름이 표시됩니다.
- 상품 이미지는 고정된 썸네일 사이즈로 제공되므로 UI 배치 시 크기 확인이 필요합니다.
