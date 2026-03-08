# 검색 > 책 - Search API

## 개요

네이버 검색의 책 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 또한 상세 검색 API(`book_adv`)를 통해 제목, 저자, ISBN 등을 지정하여 정교한 검색이 가능합니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 1. 일반 책 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/book.xml`
  - `https://openapi.naver.com/v1/search/book.json`
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String | Y | 검색어. UTF-8 인코딩 필수 |
| `display` | Integer | N | 검색 결과 개수 (1~100, 기본 10) |
| `start` | Integer | N | 검색 시작 위치 (1~1000, 기본 1) |
| `sort` | String | N | `sim` (유사도순, 기본), `date` (출간일순) |

### 2. 책 상세 검색 결과 조회 (book_adv)

책 상세 검색은 특정 조건(제목, 저자, 출판사 등)을 명시하여 검색할 때 사용합니다.

- **요청 URL**: `https://openapi.naver.com/v1/search/book_adv.xml` (또는 `.json`)
- **HTTP 메서드**: GET

#### 상세 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `d_titl` | String | N | 책 제목 |
| `d_auth` | String | N | 저자 이름 |
| `d_cont` | String | N | 목차 |
| `d_isbn` | String | N | ISBN |
| `d_publ` | String | N | 출판사 이름 |
| `d_daop` | String | N | 출간일 (YYYYMMDD 형식) |
| `d_catg` | String | N | 카테고리 코드 |
| *이 중 1개 이상의 파라미터는 반드시 포함되어야 합니다.* |

## 응답 필드

- `lastBuildDate`: 검색 결과 생성 시간
- `total`: 총 검색 결과 수
- `items`: 검색 결과 리스트
  - `title`: 책 제목
  - `link`: 네이버 도서 정보 URL
  - `image`: 섬네일 이미지 URL
  - `author`: 저자
  - `price`: 정가
  - `discount`: 할인가
  - `publisher`: 출판사
  - `pubdate`: 출간일
  - `isbn`: ISBN (10자리 또는 13자리)
  - `description`: 책 설명 요약

## 구현 예제 (Node.js)

```javascript
var express = require('express');
var app = express();
var clientId = 'YOUR_CLIENT_ID';
var clientSecret = 'YOUR_CLIENT_SECRET';

app.get('/search/book', function (req, res) {
   var api_url = 'https://openapi.naver.com/v1/search/book.json?query=' + encodeURI(req.query.query);
   var request = require('request');
   var options = {
       url: api_url,
       headers: {'X-Naver-Client-Id':Client ID, 'X-Naver-Client-Secret': Client Secret}
    };
   request.get(options, function (error, response, body) {
     if (!error && response.statusCode == 200) {
       res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8'});
       res.end(body);
     } else {
       res.status(response.statusCode).end();
       console.log('error = ' + response.statusCode);
     }
   });
 });
 app.listen(3000, function () {
   console.log('http://127.0.0.1:3000/search/book?query=주식 app listening on port 3000!');
 });
```

## 오류 코드 가이드 가이드

| 코드 | 설명 | 해결 방법 |
| :--- | :--- | :--- |
| 400 | Invalid parameter | 요청 변수의 이름이나 값이 잘못되지 않았는지 확인 |
| 401 | Authentication failed | Client ID/Secret 값이 정확한지 확인 |
| 403 | Forbidden | 애플리케이션 설정에서 해당 API 사용 신청이 되었는지 확인 |
| 429 | Quota exceeded | 일일 허용 호출량을 초과함 |
| 500 | Internal server error | 네이버 시스템 측 에러. 잠시 후 재시도 |
