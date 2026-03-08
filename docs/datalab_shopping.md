# 쇼핑인사이트 - 네이버 데이터랩

## 개요

네이버 쇼핑의 방대한 데이터를 바탕으로 분야별 클릭 추이와 검색어 현황을 분석할 수 있는 서비스입니다. 특정 카테고리의 트렌드 변화를 파악하고, 쇼핑 사용자들이 어떤 상품에 관심을 가지는지 심층적으로 분석할 수 있습니다.

## 주요 기능

### 1. 분야별 클릭 추이 (Category Insights)

- 쇼핑 카테고리별로 클릭이 발생하는 추이를 그래프로 제공합니다.
- 패션잡화, 화장품/미용, 가전/디지털 등 네이버 쇼핑의 전 카테고리를 대상으로 합니다.
- **활용**: 특정 시즌에 어떤 카테고리가 강세인지 파악하여 상품 소싱 및 마케팅 전략 수립에 활용합니다.

### 2. 검색어 현황 (Keyword Insights)

- 각 카테고리 내에서 인기 있는 검색어 순위를 제공합니다.
- 사용자가 설정한 기간, 성별, 연령대, 기기별로 필터링된 인기 검색어 TOP 500을 확인할 수 있습니다.
- **활용**: 소비자가 실제로 검색하는 키워드를 발굴하여 상세 페이지 키워드나 광고 소재로 활용합니다.

## API 레퍼런스

데이터랩 쇼핑인사이트는 개발자를 위한 RESTful API를 제공하여 데이터를 자동화된 방식으로 수집할 수 있습니다.

- **요청 URL**: `https://openapi.naver.com/v1/datalab/shopping/categories` (카테고리별 클릭 추이)
- **프로토콜**: HTTPS
- **HTTP 메서드**: POST

#### 요청 파라미터 (JSON)

| 필드명 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `startDate` | String | Y | 조회 시작 날짜 (yyyy-mm-dd) |
| `endDate` | String | Y | 조회 종료 날짜 (yyyy-mm-dd) |
| `timeUnit` | String | Y | 구간 단위 (date, week, month) |
| `category` | String | Y | 쇼핑 카테고리 코드 |
| `device` | String | N | 기기 필터 (pc, mo) |
| `gender` | String | N | 성별 필터 (m, f) |
| `ages` | Array | N | 연령대 필터 (1~11) |

## 구현 예제 (Java)

```java
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class ApiExamDatalabShopping {
    public static void main(String[] args) {
        String clientId = "YOUR_CLIENT_ID";
        String clientSecret = "YOUR_CLIENT_SECRET";

        try {
            String apiURL = "https://openapi.naver.com/v1/datalab/shopping/categories";
            String body = "{\"startDate\":\"2023-08-01\",\"endDate\":\"2023-08-30\",\"timeUnit\":\"date\",\"category\":\"50000000\"}";
            
            URL url = new URL(apiURL);
            HttpURLConnection con = (HttpURLConnection)url.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("X-Naver-Client-Id", clientId);
            con.setRequestProperty("X-Naver-Client-Secret", clientSecret);
            con.setRequestProperty("Content-Type", "application/json");

            con.setDoOutput(true);
            try (OutputStream os = con.getOutputStream()) {
                byte[] input = body.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }

            int responseCode = con.getResponseCode();
            BufferedReader br;
            if (responseCode == 200) {
                br = new BufferedReader(new InputStreamReader(con.getInputStream()));
            } else {
                br = new BufferedReader(new InputStreamReader(con.getErrorStream()));
            }

            String inputLine;
            StringBuilder response = new StringBuilder();
            while ((inputLine = br.readLine()) != null) {
                response.append(inputLine);
            }
            br.close();
            System.out.println(response.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## 주의 사항

- **카테고리 코드**: 네이버 쇼핑에서 사용하는 공식 카테고리 ID를 입력해야 합니다. (예: 50000000 - 패션잡화)
- **상대 수치**: 결과값은 조회 기간 중 최대 클릭량을 100으로 잡은 상대적 비율(Ratio)입니다.
- **데이터 업데이트**: 데이터는 매일 오전 중 전날까지의 데이터가 업데이트됩니다.
- **이용 약관**: 수집한 데이터를 외부 서비스에 노출할 경우 반드시 '네이버 데이터랩' 출처를 명시해야 합니다.

## 활용 팁

- **시즌성 상품 발굴**: 매월 초 Shopping Insight의 전년도 같은 달 키워드 순위를 분석하여 다가올 수요를 미리 예측할 수 있습니다.
- **타겟 전략**: 카테고리별로 주 구매층(성별/연령)의 클릭 비중을 분석하여 타겟 맞춤형 프로모션을 설계합니다.
