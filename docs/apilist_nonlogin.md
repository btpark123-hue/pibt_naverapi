# 비로그인 방식 오픈 API 목록 - NAVER Developers

## 개요

네이버 오픈 API 중 **비로그인 방식 API**는 별도의 사용자 로그인이 필요 없이, 애플리케이션에 발급된 **Client ID**와 **Client Secret** 키만 있으면 바로 호출할 수 있는 API들을 말합니다.

이 문서에서는 비로그인 방식으로 간단하게 연동 가능한 주요 API 리스트와 호출 공통 사항을 정리합니다.

## 주요 비로그인 API 리스트

### 1. 검색 (Search)

- **블로그 검색**: 네이버 블로그 포스트 검색 결과 조회.
- **뉴스 검색**: 네이버 뉴스 검색 결과 조회.
- **책 검색**: 도서 정보 및 상세 검색 조회.
- **쇼핑 검색**: 상품 정보 및 가격 비교 데이터 조회.
- **이미지 검색**: 고해상도 이미지 및 썸네일 수집.
- **지역 검색**: 업체, 기관 위치 및 정보 조회.
- **지식iN 검색**: 질문/답변 데이터 수집.
- **성인검색어 판별**: 검색어의 유해성 판별.
- **오타변환**: 잘못 입력된 한/영 자판 오타 교정.

### 2. 유틸리티 및 기타

- **캡차 (Captcha)**: 이미지 및 음성을 통한 봇 차단 인증 서비스.
- **네이버 공유하기**: 웹 컨텐츠를 네이버의 다양한 서비스로 공유.
- **오픈메인 (OpenMain)**: 서비스를 네이버 모바일 메인에 추가 유도.
- **파일 업로드**: 관련 서비스 내 이미지/파일 전송 기능.

### 3. 클로바 인공지능 (CLOVA)

- **Face Recognition**: 유명인 닮은꼴 인식 및 얼굴 속성 분석.

### 4. 데이터랩 (DataLab)

- **통합 검색어 트렌드**: 주제별 검색 추이 데이터 분석.
- **쇼핑인사이트**: 카테고리별 클릭량 및 인기 검색어 추이.

## 공통 인증 및 호출 규격

비로그인 API는 모든 요청에 대해 아래 정보를 HTTP 헤더에 포함해야 합니다.

### HTTP 헤더 설정

| 헤더 필드명 | 설명 |
| :--- | :--- |
| `X-Naver-Client-Id` | 내 애플리케이션 등록 시 발급받은 Client ID |
| `X-Naver-Client-Secret` | 내 애플리케이션 등록 시 발급받은 Client Secret |
| `Content-Type` | 데이터 전송 방식 (주로 `application/json` 또는 `application/x-www-form-urlencoded`) |

### 호출 예시 (cURL)

```bash
curl "https://openapi.naver.com/v1/search/blog?query={SEARCH_TEXT}" \
    -H "X-Naver-Client-Id: {YOUR_CLIENT_ID}" \
    -H "X-Naver-Client-Secret: {YOUR_CLIENT_SECRET}"
```

## 이용 가이드 및 제한

### 1. 애플리케이션 등록

- [네이버 개발자 센터] -> [Application] -> [애플리케이션 등록]에서 원하는 API 권한을 선택하여 등록해야 합니다.

### 2. 일일 호출 한도 (Quota)

- 비로그인 API는 애플리케이션 레벨에서 일일 호출 횟수가 제한됩니다.
- 검색 API: 전체 통합 일 25,000건.
- 캡차 API: 일 10,000건.
- 데이터랩 API: 일 1,000건.
- 한도 초과 시 **429 (Too Many Requests)** 에러가 발생하며, 익일 자정(KST)에 초기화됩니다.

### 3. 데이터 활용 주의 사항

- 네이버 API에서 제공하는 데이터는 개인적인 분석이나 서비스 제공 용도로 활용 가능하나, 수집된 데이터를 통한 대규모 DB 구축이나 재판매는 금지될 수 있습니다.
- 상세한 규정은 [API 이용약관](file:///c:/naver_api/docs/apiterms.md)을 참조하세요.

## 오류 코드 가이드 가이드 (Common Errors)

| 상태 코드 | 에러 메시지 | 원인 및 해결 방법 |
| :--- | :--- | :--- |
| 401 | Verification failed | Client ID 또는 Secret이 정확하지 않음. |
| 403 | Forbidden | 애플리케이션 설정에서 해당 API 권한을 체크했는지 확인. |
| 404 | Not Found | API 호출 주소(URL)가 원본 문서와 동일한지 확인. |
| 500 | Internal Server Error | 네이버 시스템 장애. 잠시 기다린 후 재시도. |

## 문서 이동 가이드

각 API의 상세 구현 방법은 `docs` 폴더 내의 개별 마크다운 파일을 참조하시기 바랍니다.

- **블로그 구현**: [blog.md](file:///c:/naver_api/docs/blog.md)
- **뉴스 구현**: [news.md](file:///c:/naver_api/docs/news.md)
- **캡차 구현**: [captcha_image.md](file:///c:/naver_api/docs/captcha_image.md)
- **데이터랩 구현**: [datalab_search_trend.md](file:///c:/naver_api/docs/datalab_search_trend.md)
