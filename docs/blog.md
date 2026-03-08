# 검색 > 블로그 - Search API

## 개요

네이버 검색의 블로그 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다. 비로그인 방식 오픈 API이므로 호출 시 HTTP 헤더에 **Client ID**와 **Client Secret** 값만 전송하면 됩니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## API 레퍼런스

### 블로그 검색 결과 조회

- **요청 URL**:
  - `https://openapi.naver.com/v1/search/blog.xml` (XML 응답)
  - `https://openapi.naver.com/v1/search/blog.json` (JSON 응답)
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 여부 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String (UTF-8) | 필수 | 검색어. UTF-8로 인코딩되어야 합니다. |
| `display` | Integer | 선택 | 한 번에 표시할 검색 결과 개수 (기본값: 10, 최댓값: 100) |
| `start` | Integer | 선택 | 검색 시작 위치 (기본값: 1, 최댓값: 1000) |
| `sort` | String | 선택 | 정렬 옵션: `sim` (유사도순, 기본값), `date` (날짜순) |

#### 응답 필드

- `lastBuildDate`: datetime. 검색 결과를 생성한 시간
- `total`: integer. 총 검색 결과 개수
- `start`: integer. 검색 시작 위치
- `display`: integer. 한 번에 표시할 검색 결과 개수
- `items`: XML/JSON 형식의 개별 검색 결과
  - `title`: string. 블로그 포스트의 제목. (HTML 태그 포함 가능)
  - `link`: string. 블로그 포스트의 URL
  - `description`: string. 블로그 포스트의 요약 내용
  - `bloggername`: string. 블로그의 이름
  - `bloggerlink`: string. 블로그의 주소
  - `postdate`: string. 블로그 포스트가 작성된 날짜

## 구현 예제 (Java)

```java
import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

public class ApiExamSearchBlog {
    public static void main(String[] args) {
        String clientId = "YOUR_CLIENT_ID"; //애플리케이션 **Client ID**
        String clientSecret = "YOUR_CLIENT_SECRET"; //애플리케이션 **Client Secret**

        String text = null;
        try {
            text = URLEncoder.encode("그린팩토리", "UTF-8");
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException("검색어 인코딩 실패",e);
        }

        String apiURL = "https://openapi.naver.com/v1/search/blog?query=" + text; // JSON 결과

        Map<String, String> requestHeaders = new HashMap<>();
        requestHeaders.put("X-Naver-Client-Id", clientId);
        requestHeaders.put("X-Naver-Client-Secret", clientSecret);
        String responseBody = get(apiURL,requestHeaders);

        System.out.println(responseBody);
    }

    private static String get(String apiUrl, Map<String, String> requestHeaders){
        HttpURLConnection con = connect(apiUrl);
        try {
            con.setRequestMethod("GET");
            for(Map.Entry<String, String> header :requestHeaders.entrySet()) {
                con.setRequestProperty(header.getKey(), header.getValue());
            }

            int responseCode = con.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) { // 정상 호출
                return readBody(con.getInputStream());
            } else { // 오류 발생
                return readBody(con.getErrorStream());
            }
        } catch (IOException e) {
            throw new RuntimeException("API 요청과 응답 실패", e);
        } finally {
            con.disconnect();
        }
    }

    private static HttpURLConnection connect(String apiUrl){
        try {
            URL url = new URL(apiUrl);
            return (HttpURLConnection)url.openConnection();
        } catch (MalformedURLException e) {
            throw new RuntimeException("API URL이 잘못되었습니다. : " + apiUrl, e);
        } catch (IOException e) {
            throw new RuntimeException("연결이 실패했습니다. : " + apiUrl, e);
        }
    }

    private static String readBody(InputStream body){
        InputStreamReader streamReader = new InputStreamReader(body);

        try (BufferedReader lineReader = new BufferedReader(streamReader)) {
            StringBuilder responseBody = new StringBuilder();

            String line;
            while ((line = lineReader.readLine()) != null) {
                responseBody.append(line);
            }

            return responseBody.toString();
        } catch (IOException e) {
            throw new RuntimeException("API 응답을 읽는 데 실패했습니다.", e);
        }
    }
}
```

## 오류 코드 가이드

- **400**: 잘못된 요청 (파라미터 오류 등)
- **401**: 인증 실패 (Client ID/Secret 오류)
- **403**: 권한 없음 (API 설정 미비 등)
- **404**: 요청한 URL을 찾을 수 없음
- **500**: 내부 서버 오류
