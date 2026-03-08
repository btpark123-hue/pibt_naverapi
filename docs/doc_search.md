# 검색 > 전문자료 - Search API

## 개요

네이버 검색의 전문 자료(학술 논문, 학위 논문, 학술 잡지 등) 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 연구 자료 및 학술 문헌 정보를 효율적으로 검색할 수 있습니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 전문 자료 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/doc.xml`
  - `https://openapi.naver.com/v1/search/doc.json`
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String | Y | 검색어 (UTF-8 인코딩) |
| `display` | Integer | N | 결과 개수 (1~100, 기본 10) |
| `start` | Integer | N | 검색 시작 위치 (1~1000, 기본 1) |

#### 응답 필드

- `lastBuildDate`: 검색 결과 생성 시간
- `total`: 검색된 총 논문/자료 수
- `items`: 개별 검색 결과 리스트
  - `title`: 논문 또는 자료의 제목 (HTML `<b>` 태그 포함 가능)
  - `link`: 해당 자료의 상세 페이지 URL
  - `description`: 논문 요약 정보 혹은 서지 정보의 일부

## 구현 예제 (Java)

```java
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

public class ApiExamSearchDoc {
    public static void main(String[] args) {
        String clientId = "YOUR_CLIENT_ID";
        String clientSecret = "YOUR_CLIENT_SECRET";
        try {
            String text = URLEncoder.encode("인공지능", "UTF-8");
            String apiURL = "https://openapi.naver.com/v1/search/doc.json?query=" + text;
            URL url = new URL(apiURL);
            HttpURLConnection con = (HttpURLConnection)url.openConnection();
            con.setRequestMethod("GET");
            con.setRequestProperty("X-Naver-Client-Id", clientId);
            con.setRequestProperty("X-Naver-Client-Secret", clientSecret);
            
            int responseCode = con.getResponseCode();
            BufferedReader br;
            if(responseCode == 200) {
                br = new BufferedReader(new InputStreamReader(con.getInputStream()));
            } else {
                br = new BufferedReader(new InputStreamReader(con.getErrorStream()));
            }
            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = br.readLine()) != null) {
                response.append(inputLine);
            }
            br.close();
            System.out.println(response.toString());
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
```

## 응답 예시 (XML)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Naver Open API - doc ::'주식'</title>
  <link>http://search.naver.com</link>
  <description>Naver Search Result</description>
  <lastBuildDate>Mon, 26 Sep 2016 10:44:34 +0900</lastBuildDate>
  <total>20135</total>
  <start>1</start>
  <display>10</display>
  <item>
    <title>차등의결권 &lt;b&gt;주식&lt;/b&gt;의 도입에 관한 법적 연구</title>
    <link>http://openapi.naver.com/l?AAABW...</link>
    <description>제1장 서 론 1 제1절 연구의 목적 1 제2절 연구 방법 3...</description>
  </item>
</channel>
</rss>
```

## 오류 코드 가이드 가이드

| 에러 코드 | 원인 및 해결 |
| :--- | :--- |
| 400 (SE01) | query 파라미터 누락 |
| 401 (401) | 유효하지 않은 계정 정보 (Client ID/Secret 재확인) |
| 403 (403) | 검색 API 사용 신청 안 됨 혹은 일일 허용량 초가 |
| 500 (500) | 네이버 서버 응답 지연 혹은 장애 |

## 활용 시 유의사항

- 전문 자료 검색 결과는 주로 학계 자료이므로 일반 뉴스나 블로그 결과보다 전문적인 내용이 많습니다.
- `link` 정보를 통해 전문 자료 제공 사이트로 이동하여 유료/무료 여부를 확인해야 할 수도 있습니다.
- 대용량 검색 시에는 `start`와 `display` 파라미터를 적절히 이용해 시스템 부하를 줄여야 합니다.
