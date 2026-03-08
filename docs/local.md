# 검색 > 지역 - Search API

## 개요

네이버 지역 서비스에 등록된 업체 및 기관을 검색한 결과를 XML 또는 JSON 형식으로 반환하는 RESTful API입니다. 음식점, 카페, 병원 등 장소 정보를 검색하여 지도 서비스나 위치 기반 서비스에 활용할 수 있습니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 지역 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/local.xml`
  - `https://openapi.naver.com/v1/search/local.json`
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String | Y | 검색어 (UTF-8 인코딩) |
| `display` | Integer | N | 검색 결과 개수 (1~5, 기본 1) |
| `start` | Integer | N | 검색 시작 위치 (1~1) |
| `sort` | String | N | 정렬 옵션<br>- `random`: 유사도순 (기본값)<br>- `comment`: 카페/블로그 리뷰 개수순 |

#### 응답 필드

| 필드명 | 설명 |
| :--- | :--- |
| `title` | 업체/기관명 |
| `link` | 상세 정보 페이지 URL |
| `category` | 카데고리 정보 |
| `description` | 업체 상세 설명 |
| `telephone` | 전화번호 |
| `address` | 지번 주소 |
| `roadAddress` | 도로명 주소 |
| `mapx`, `mapy` | 지도 좌표 (KATECH 좌표계) |

## 구현 예제 (Java)

```java
// 검색 - 지역 검색 예제
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

public class ApiExamSearchLocal {
    public static void main(String[] args) {
        String clientId = "YOUR_CLIENT_ID";
        String clientSecret = "YOUR_CLIENT_SECRET";
        try {
            String text = URLEncoder.encode("을지로 맛집", "UTF-8");
            String apiURL = "https://openapi.naver.com/v1/search/local.json?query=" + text;
            URL url = new URL(apiURL);
            HttpURLConnection con = (HttpURLConnection)url.openConnection();
            con.setRequestMethod("GET");
            con.setRequestProperty("X-Naver-Client-Id", clientId);
            con.setRequestProperty("X-Naver-Client-Secret", clientSecret);
            int responseCode = con.getResponseCode();
            BufferedReader br;
            if(responseCode==200) { br = new BufferedReader(new InputStreamReader(con.getInputStream())); }
            else { br = new BufferedReader(new InputStreamReader(con.getErrorStream())); }
            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = br.readLine()) != null) { response.append(inputLine); }
            br.close();
            System.out.println(response.toString());
        } catch (Exception e) { System.out.println(e); }
    }
}
```

## 응답 예시 (XML)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Naver Open API - local ::'갈비집'</title>
  <link>http://search.naver.com</link>
  <description>Naver Search Result</description>
  <lastBuildDate>Tue, 04 Oct 2016 13:10:58 +0900</lastBuildDate>
  <total>407</total>
  <start>1</start>
  <display>10</display>
  <item>
    <title>조선옥</title>
    <link />
    <category>한식&gt;육류,고기요리</category>
    <description>연탄불 한우갈비 전문점.</description>
    <telephone>02-2266-0333</telephone>
    <address>서울특별시 중구 을지로3가 229-1 </address>
    <roadAddress>서울특별시 중구 을지로15길 6-5 </roadAddress>
    <mapx>311277</mapx>
    <mapy>552097</mapy>
  </item>
</channel>
</rss>
```

## 주의 사항

- **좌표계**: 응답되는 `mapx`, `mapy` 정보는 네이버 지도에서 사용하는 **KATECH** 좌표계입니다. 위경도(WGS84) 좌표로 사용하려면 별도의 변환 라이브러리나 API를 사용해야 합니다.
- **주소 정보**: 구 주소(`address`)와 신 주소(`roadAddress`)가 함께 제공됩니다.
- **호출 제한**: 검색 API 일 통합 25,000건 한도 내에서 사용 가능합니다.
- **분류**: `category` 필드를 통해 해당 장소의 상세 분류 정보를 얻을 수 있습니다.
