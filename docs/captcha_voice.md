# 유틸리티 > 캡차(음성) - Captcha API

## 개요

네이버 캡차(음성) API는 시각 장애가 있는 사용자나 이미지를 보기 어려운 환경에 있는 사용자를 위해 캡차 코드를 음성(MP3)으로 들려주는 보안 서비스입니다.

사용자가 들은 숫자를 입력하면 서버에서 인증 여부를 판별하며, 주로 이미지 캡차의 대체 수단이나 접근성 향상을 위해 사용됩니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)

## 인증 프로세스

음성 캡차 구현은 다음 3가지 단계를 거칩니다.

### Step 1: 캡차 키 발급 (Key Issuance)

음성 캡차용 세션 키를 생성합니다.

- **URL**: `https://openapi.naver.com/v1/captcha/nkey?code=0`
- **Method**: GET
- **응답**: `{"key":"고유키값"}`

### Step 2: 음성 파일 생성 및 재생 (Audio Streaming)

발급받은 키를 사용하여 숫자를 읽어주는 MP3 파일을 스트리밍하거나 내려받습니다.

- **URL**: `https://openapi.naver.com/v1/captcha/scaptcha.bin?key={key}`
- **Method**: GET
- **응답**: 오디오 데이터 (MPEG/MP3 형식)

### Step 3: 사용자 입력값 검증 (Key Verification)

사용자가 청취 후 입력한 값과 키를 대조하여 성공 여부를 확인합니다.

- **URL**: `https://openapi.naver.com/v1/captcha/nkey?code=1&key={key}&value={user_input}`
- **Method**: GET
- **응답**: `{"result":true}` 또는 `{"result":false}`

## API 상세 파라미터

### 캡차 키 발급 API (code=0)

| 파라미터 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `code` | Integer | Y | `0`: 키 발급 요청 |

### 캡차 음성 전송 API

| 파라미터 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `key` | String | Y | 발급받은 캡차 키값 |

### 캡차 키 검증 API (code=1)

| 파라미터 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `code` | Integer | Y | `1`: 키 검증 요청 |
| `key` | String | Y | 발급받은 캡차 키값 |
| `value` | String | Y | 사용자가 입력한 숫자 조합 |

## 구현 예제 (Node.js)

```javascript
var express = require('express');
var app = express();
var clientId = 'YOUR_CLIENT_ID';
var clientSecret = 'YOUR_CLIENT_SECRET';
var fs = require('fs');

app.get('/captcha/voice', function (req, res) {
   var api_url = 'https://openapi.naver.com/v1/captcha/nkey?code=0';
   var request = require('request');
   var options = {
       url: api_url,
       headers: {'X-Naver-Client-Id':Client ID, 'X-Naver-Client-Secret': Client Secret}
    };
    
   // 1. 키 발급 요청
   request.get(options, function (error, response, body) {
     if (!error && response.statusCode == 200) {
       var key = JSON.parse(body).key;
       
       // 2. 음성 파일 요청 및 저장
       var voice_url = 'https://openapi.naver.com/v1/captcha/scaptcha.bin?key=' + key;
       var file_options = {
           url: voice_url,
           headers: {'X-Naver-Client-Id':Client ID, 'X-Naver-Client-Secret': Client Secret}
       };
       var writeStream = fs.createWriteStream('./captcha.mp3');
       request.get(file_options).pipe(writeStream);
       
       writeStream.on('finish', function () {
           res.send('음성 파일(captcha.mp3)이 저장되었습니다. 키: ' + key);
       });
     } else {
       res.status(response.statusCode).end();
       console.log('error = ' + response.statusCode);
     }
   });
 });

 app.listen(3000, function () {
   console.log('Voice Captcha Example app listening on port 3000!');
 });
```

## 오류 코드 가이드 요약

| 코드 | 메시지 | 원인 및 해결 |
| :--- | :--- | :--- |
| 401 | Invalid Key | Client ID/Secret을 다시 확인하세요. |
| 403 | Forbidden | API 설정에서 캡차 서비스 신청 여부를 확인하세요. |
| 404 | Not Found | 요청한 URL이 정확한지 확인하세요. |
| 500 | System Error | 네이버 시스템 측 장애입니다. |

## 개발 팁 및 유의사항

- **웹 접근성**: 시각 장애인 사용자를 위해 `alt="음성 캡차 듣기"` 속성이 있는 버튼을 제공하는 것을 권장합니다.
- **포맷 지원**: 브라우저의 `<audio>` 태그를 사용하면 별도의 플레이어 구현 없이 간편하게 재생할 수 있습니다.
- **수명 주기**: 발급된 키는 보안상 일정 시간(보통 수 분)이 지나면 만료되므로 주의하십시오.
- **이미지 캡차와 결합**: 일반적으로 이미지 캡차 옆에 "음성으로 듣기" 버튼을 배치하여 사용자가 선택하게 합니다.
