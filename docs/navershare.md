# 유틸리티 > 네이버 공유하기 - Share API

## 개요

네이버 공유하기는 사용자가 여러분의 컨텐츠(웹 페이지, 블로그 포스트 등)를 네이버 서비스(블로그, 카페, 포스트, LINE 등)로 간편하게 공유할 수 있게 해주는 기능입니다.

간단한 URL 링크 방식 또는 자바스크립트 기반의 플러그인 방식을 통해 구현할 수 있으며, 모바일과 PC 환경을 모두 지원합니다.

### 주요 특징

- **간편한 연동**: 복잡한 API 권한 신청 없이 클라이언트 단에서 즉시 구현 가능합니다.
- **다양한 서비스 지원**: 네이버 블로그, 카페, 포스트, 메일 및 LINE 등으로 공유를 지원합니다.
- **커스터마이징 가능**: 네이버 제공 아이콘 외에도 서비스 디자인에 맞는 커스텀 버튼을 사용할 수 있습니다.

## 구현 방법

### 방법 1: URL 링크 방식 (권장)

가장 간단한 방법으로, 특정 URL로 사용자를 이동시켜 공유 창을 띄웁니다.

- **요청 URL**: `https://share.naver.com/web/shareView`
- **프로토콜**: HTTPS
- **HTTP 메서드**: GET

#### 요청 파라미터

| 매개변수 | 타입 | 필수 여부 | 설명 |
| :--- | :--- | :--- | :--- |
| `url` | String | 필수 | 공유할 웹 페이지의 URL. 반드시 **UTF-8로 인코딩**되어야 합니다. |
| `title` | String | 필수 | 공유될 때 표시될 제목. 반드시 **UTF-8로 인코딩**되어야 합니다. |

#### 구현 예시 (HTML/JavaScript)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>네이버 공유하기 예제</title>
    <script>
        function shareToNaver() {
            // 공유할 URL과 제목 설정
            var url = encodeURIComponent(window.location.href);
            var title = encodeURIComponent(document.title);
            
            // 공유 창 호출 URL 생성
            var shareURL = "https://share.naver.com/web/shareView?url=" + url + "&title=" + title;
            
            // 새 창으로 열기 (권장) 또는 현재 창 이동
            window.open(shareURL, 'naver_share', 'width=500, height=500');
        }
    </script>
</head>
<body>
    <h3>내 컨텐츠 공유하기</h3>
    <!-- 커스텀 버튼 사용 예시 -->
    <button onclick="shareToNaver()">
        네이버로 공유하기
    </button>
</body>
</html>
```

### 방법 2: 플러그인 방식 (버튼 스크립트)

네이버에서 제공하는 공식 자바스크립트 라이브러리를 사용하여 표준화된 버튼을 생성합니다.

#### 라이브러리 로드

```html
<script type="text/javascript" src="https://ssl.pstatic.net/share/js/naver_sharebutton.js"></script>
```

#### 버튼 생성 스크립트

```html
<script type="text/javascript">
    new ShareNaver.makeButton({
        "type": "a", // 버튼 타입 (a, b, c, d, e, f 등 지원)
        "title": "공유할 제목", // (선택) 생략 시 현재 페이지 title 사용
        "url": "https://example.com" // (선택) 생략 시 현재 페이지 URL 사용
    });
</script>
```

## 주의 사항 및 팁

### 1. 인코딩 주의

`url`과 `title` 파라미터는 반드시 `encodeURIComponent()` 등을 통해 UTF-8 인코딩 처리를 해야 합니다. 인코딩이 누락될 경우 한글 깨짐이나 링크 오류가 발생할 수 있습니다.

**바른 예:**
`https://share.naver.com/web/shareView?url=https%3A%2F%2Fexample.com&title=%ED%85%84%ED%8A%B8`

**잘못된 예:**
`https://share.naver.com/web/shareView?url=https://example.com&title=테스트`

### 2. 로컬 개발 환경

공유하려는 URL이 `localhost`나 `127.0.0.1`과 같은 로컬 경로일 경우, 네이버 서버에서 해당 URL의 메타 정보를 수집할 수 없어 미리보기 이미지가 나오지 않거나 공유가 실패할 수 있습니다. 실제 배포된 도메인에서 테스트하시기 바랍니다.

### 3. Open Graph (og) 태그 설정

공유 시 보여지는 이미지, 설명, 제목 등은 공유 창 내부에서 해당 URL의 OG 태그를 파싱하여 보여줍니다. 원활한 홍보를 위해 아래 태그를 원본 페이지에 삽입하는 것을 권장합니다.

```html
<meta property="og:title" content="컨텐츠 제목" />
<meta property="og:description" content="컨텐츠 요약 설명" />
<meta property="og:image" content="https://example.com/thumbnail.jpg" />
<meta property="og:url" content="https://example.com" />
```

### 4. 디자인 가이드

네이버 공유 버튼 이미지를 직접 제작하여 사용하고 싶다면, 네이버 브랜드 가이드를 준수해야 합니다.

- [공식 아이콘 다운로드 (ZIP)](https://ssl.pstatic.net/share/download/NAVER_SQUARE_Logo.zip)
- [N스퀘어 가이드 다운로드 (ZIP)](https://ssl.pstatic.net/share/download/NAVER_SQUARE_Guide.zip)

## FAQ

- **Q: 공유 팝업이 차단됩니다.**
  - A: `window.open`은 사용자의 클릭 이벤트 내에서 호출되어야 브라우저 팝업 차단에 걸리지 않습니다.
- **Q: 이미지가 안 나옵니다.**
  - A: 공유할 페이지의 `<meta property="og:image">` 태그가 올바른 이미지 URL을 가리키고 있는지 확인하세요.
