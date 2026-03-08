# 검색 > 백과사전 - Search API

## 개요

네이버 검색의 백과사전 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 네이버 지식백과의 방대한 전문 지식 데이터를 기반으로 정확하고 검증된 용어 정의와 상세 설명을 제공합니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 백과사전 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/encyc.xml` (XML)
  - `https://openapi.naver.com/v1/search/encyc.json` (JSON)
- **HTTP 메서드**: GET
- **인증 방식**: HTTP Header (X-Naver-Client-Id, X-Naver-Client-Secret)

#### 요청 파라미터

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String | Y | 검색어 (UTF-8 인코딩 필수) |
| `display` | Integer | N | 한 번에 표시할 결과 개수 (1~100, 기본 10) |
| `start` | Integer | N | 검색 시작 위치 (1~1000, 기본 1) |

#### 응답 필드

| 필드명 | 설명 |
| :--- | :--- |
| `lastBuildDate` | 검색 결과 생성 일시 |
| `total` | 총 검색 결과 개수 |
| `results` | 검색 결과 리스트 |
| - `title` | 사전 표제어 (HTML 태그 포함 가능) |
| - `link` | 네이버 지식백과 상세 정보 URL |
| - `description` | 사전 내용 요약 (HTML 태그 포함 가능) |
| - `thumbnail` | 대표 이미지 섬네일 URL |

## 구현 예제 (Java)

```java
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

public class ApiExamSearchEncyc {
    public static void main(String[] args) {
        String clientId = "YOUR_CLIENT_ID";
        String clientSecret = "YOUR_CLIENT_SECRET";
        
        try {
            String text = URLEncoder.encode("양자역학", "UTF-8");
            String apiURL = "https://openapi.naver.com/v1/search/encyc.json?query=" + text;
            
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
    <title>Naver Open API - encyc ::'양자역학'</title>
    <link>http://search.naver.com</link>
    <description>Naver Search Result</description>
    <lastBuildDate>Mon, 26 Sep 2016 11:23:45 +0900</lastBuildDate>
    <total>421</total>
    <start>1</start>
    <display>10</display>
    <item>
      <title>&lt;b&gt;양자역학&lt;/b&gt; [quantum mechanics]</title>
      <link>http://terms.naver.com/entry.nhn?docId=1124439...</link>
      <description>분자, 원자, 소립자와 같은 미시적인 대상의 역학을 설명하는...</description>
      <thumbnail>http://openapi.naver.com/l?AAAB2O...</thumbnail>
    </item>
  </channel>
</rss>
```

## 주요 오류 코드

| 코드 | 메시지 | 해결 방법 |
| :--- | :--- | :--- |
| 400 | Query missing | `query` 파라미터가 비어있지 않은지 확인하세요. |
| 401 | Invalid Client ID | 등록한 애플리케이션의 Client ID를 재확인하세요. |
| 403 | API Forbidden | 검색 API 권한이 활성화되어 있는지 확인하세요. |
| 429 | Quota EXceeded | 일일 검색 호출 한도(25,000건) 초과 여부를 확인하세요. |

## 활용 팁

- **전문성 확보**: 블로그나 뉴스 검색 결과에 비해 검증된 학술적 정의가 필요할 때 지식백과 API를 병행하여 사용하면 서비스의 성숙도를 높일 수 있습니다.
- **이미지 활용**: `thumbnail` 필드를 통해 해당 용어를 시각적으로 설명할 수 있는 이미지를 함께 노출할 수 있습니다.
- **상세 페이지 연결**: `link`를 활용해 사용자에게 더 깊이 있는 정보를 제공할 수 있도록 네이버 지식백과의 상세 항목으로 연결해 주세요.
- **다국어 대응**: 영일중 등 외국어 사전 데이터도 백과사전 검색 결과에 포함될 수 있습니다.
