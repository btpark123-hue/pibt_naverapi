# 유틸리티 > 캡차(이미지) - Captcha API

## 개요

네이버 캡차(Captcha) API는 웹 서비스나 애플리케이션에서 자동화된 봇(Bot)의 접근을 차단하고 사용자가 실제 사람인지 판별하기 위해 사용되는 보안 기능입니다. 이미지 캡차는 왜곡된 문자가 포함된 이미지를 사용자에게 보여주고, 사용자가 해당 문자를 정확히 입력하면 인증에 성공하는 방식입니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)
- [검색 API 전체 공통 개요](file:///c:/naver_api/docs/search_overview.md)

## 인증 프로세스

이미지 캡차 구현은 총 2단계로 진행됩니다.

### Step 1: 키 발급 (Key Issuance)

캡차 세션을 생성하고 고유한 키 값을 발급받습니다.

- **URL**: `https://openapi.naver.com/v1/captcha/nkey?code=0`
- **Method**: GET
- **응답**: `{"key":"발급받은키값"}`

### Step 2: 이미지 출력 (Image Display)

발급받은 키를 사용하여 캡차 이미지를 사용자에게 노출합니다.

- **URL**: `https://openapi.naver.com/v1/captcha/ncaptcha.bin?key={key}`
- **Method**: GET
- **응답**: 이미지 데이터 (JPEG/PNG)

### Step 3: 사용자 입력값 검증 (Validation)

사용자가 입력한 문자열과 발급 키를 네이버 서버로 보내 정답 여부를 확인합니다.

- **URL**: `https://openapi.naver.com/v1/captcha/nkey?code=1&key={key}&value={user_input}`
- **Method**: GET
- **응답**: `{"result":true, "responseTime":123}` 또는 `{"result":false}`

## API 상세 레퍼런스

### 1. 캡차 키 발급 API

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `code` | Integer | Y | `0` (키 발급 시 필수 값) |

### 2. 캡차 이미지 전송 API

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `key` | String | Y | Step 1에서 발급받은 키값 |

### 3. 캡차 키 검증 API

| 매개변수 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `code` | Integer | Y | `1` (키 검증 시 필수 값) |
| `key` | String | Y | Step 1에서 발급받은 키값 |
| `value` | String | Y | 사용자가 입력한 캡차 문자열 |

## 구현 예제 (Python)

```python
import os
import sys
import urllib.request
import json

clientId = "YOUR_CLIENT_ID"
clientSecret = "YOUR_CLIENT_SECRET"

# 1. 키 발급
url_key = "https://openapi.naver.com/v1/captcha/nkey?code=0"
request = urllib.request.Request(url_key)
request.add_header("X-Naver-Client-Id", clientId)
request.add_header("X-Naver-Client-Secret", clientSecret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if rescode == 200:
    res_body = response.read()
    key = json.loads(res_body.decode('utf-8'))['key']
    print("Captch Key: ", key)
    
    # 2. 이미지 저장
    url_img = "https://openapi.naver.com/v1/captcha/ncaptcha.bin?key=" + key
    urllib.request.urlretrieve(url_img, "captcha.jpg")
    print("이미지를 저장했습니다 (captcha.jpg)")
    
    # 3. 사용자 입력 검증 (예시)
    user_val = input("이미지에 보이는 문자를 입력하세요: ")
    url_check = f"https://openapi.naver.com/v1/captcha/nkey?code=1&key={key}&value={user_val}"
    req_check = urllib.request.Request(url_check)
    req_check.add_header("X-Naver-Client-Id", clientId)
    req_check.add_header("X-Naver-Client-Secret", clientSecret)
    res_check = urllib.request.urlopen(req_check)
    print(res_check.read().decode('utf-8'))
else:
    print("Error Code:" + str(rescode))
```

## 오류 코드 가이드 및 해결

- **401**: Client ID/Secret 오류. 등록한 앱 정보를 재확인하세요.
- **403**: API 권한 미설정. [API 설정] 탭에서 '캡차'가 체크되었는지 확인하세요.
- **429**: 호출 한도 초과. 이미지 캡차는 일 10,000건 한도로 제공됩니다.
- **500**: 네이버 서버 내부 오류. 네트워크 상태를 점검하거나 잠시 후 시도하세요.

## 보안 권장 사항

- 캡차 이미지는 1회용입니다. 한 번 검증에 실패하면 새로운 키를 발급받아야 보안성을 확보할 수 있습니다.
- 이미지 출력 시 캐싱(Caching)을 방지하기 위해 URL 뒤에 랜덤한 쿼리 파라미터를 추가하는 것이 좋습니다.
- 회원가입, 로그인 5회 실패, 고객 문의 글쓰기 등 민감한 동작에 적용하는 것이 효과적입니다.
