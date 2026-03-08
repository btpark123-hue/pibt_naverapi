# 검색 > 성인 검색어 판별 - Search API

## 개요

입력한 검색어가 성인 검색어인지 판별한 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 웹사이트 내에서 유해 컨텐츠 필터링이나 검색어 제한 기능을 구현할 때 유용하게 사용할 수 있습니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 성인 검색어 판별 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/adult.xml`
  - `https://openapi.naver.com/v1/search/adult.json`
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String (UTF-8) | 필수 | 판별할 검색어. 반드시 UTF-8로 인코딩되어야 합니다. |

#### 응답 필드

| 필드명 | 타입 | 설명 |
| :--- | :--- | :--- |
| `adult` | integer | 성인 검색어 여부 결과<br> - `0`: 일반 검색어<br> - `1`: 성인 검색어 |

## 응답 예시 (JSON)

```json
{
  "result": {
    "item": [
      {
        "adult": "0"
      }
    ]
  }
}
```

## 구현 예제 (PHP)

```php
<?php
  $clientId = "YOUR_CLIENT_ID";
  $clientSecret = "YOUR_CLIENT_SECRET";
  $encText = urlencode("성인검색어테스트");
  $url = "https://openapi.naver.com/v1/search/adult.json?query=".$encText;

  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

  $headers = array();
  $headers[] = "X-Naver-Client-Id: ".$Client ID;
  $headers[] = "X-Naver-Client-Secret: ".$Client Secret;
  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

  $response = curl_exec ($ch);
  $status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
  echo "status_code:".$status_code."<br>";
  curl_close ($ch);

  if($status_code == 200) {
    echo $response;
  } else {
    echo "Error 내용:".$response;
  }
?>
```

## 오류 코드 가이드

- **400 (Bad Request)**: `query` 파라미터가 누락되었거나 한글 인코딩이 잘못된 경우 발생합니다.
- **401 (Unauthorized)**: 발급받은 Client ID 또는 Client Secret 값이 잘못되었을 때 발생합니다.
- **403 (Forbidden)**: 등록된 애플리케이션 정보에서 API 서비스 사용 설정이 누락되었거나 호출 한도를 초과했을 때 발생합니다.
- **500 (Internal Server Error)**: 시스템 장애 혹은 네트워크 오류가 있는 경우 발생합니다.

## 개발 팁

- 검색어에 특수문자가 포함된 경우 인코딩 과정에서 주의가 필요합니다.
- 성인 여부 판별 결과(`0` 또는 `1`)에 따라 사용자에게 경고 메시지를 보여주거나 검색 결과를 차단하는 로직을 추가할 수 있습니다.
- 일 호출 한도는 기본 25,000건(검색 API 전체 통합)임을 유의하세요.
