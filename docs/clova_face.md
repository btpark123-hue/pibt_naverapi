# CLOVA Face Recognition (얼굴 인식) - API 가이드

## 개요

네이버 CLOVA Face Recognition API는 이미지 속의 얼굴을 인식하여 닮은 연예인을 찾거나(Celebrity), 얼굴의 감정, 나이, 성별 등 다양한 정보를 분석(Face)하는 기능을 제공하는 RESTful API입니다.

딥러닝 기반의 정교한 얼굴 분석 기술을 통해 다양한 소셜 서비스나 엔터테인먼트 앱 등에 활용할 수 있습니다.

## 주요 기능

### 1. 유명인 닮은꼴 찾기 (Celebrity)

- 입력된 이미지 속 얼굴이 어떤 유명인과 얼마나 닮았는지 분석합니다.
- 닮은 유명인의 이름과 닮은 확률(Confidence)을 반환합니다.

### 2. 얼굴 감정 및 속성 분석 (Face)

- 이미지 속 얼굴의 위치(Bounding Box)를 식별합니다.
- 성별, 연령대, 감정(기쁨, 슬픔, 화남 등), 랜드마크(눈, 코, 입 위치)를 분석하여 반환합니다.

## 사전 준비 사항
네이버 오픈 API를 호출하기 위해서는 먼저 애플리케이션을 등록하고 인증 회 키를 발급받아야 합니다. 상세한 방법은 아래 문서를 참조하십시오.
- [애플리케이션 등록 및 인증 키 발급 가이드](file:///c:/naver_api/docs/appregister.md)

## API 레퍼런스

### 유명인 인식 API

- **요청 URL**: `https://openapi.naver.com/v1/vision/celebrity`
- **HTTP 메서드**: POST
- **Content-Type**: `multipart/form-data`

### 얼굴 분석 API

- **요청 URL**: `https://openapi.naver.com/v1/vision/face`
- **HTTP 메서드**: POST
- **Content-Type**: `multipart/form-data`

#### 요청 파라미터

| 필드명 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `image` | binary | Y | 분석할 얼굴 이미 파일 (최대 2MB) |

## 구현 예제 (Python)

```python
import os
import sys
import requests

clientId = "YOUR_CLIENT_ID"
clientSecret = "YOUR_CLIENT_SECRET"

url = "https://openapi.naver.com/v1/vision/celebrity" # 닮은꼴 인식
# url = "https://openapi.naver.com/v1/vision/face" # 얼굴 분석

files = {'image': open('my_face_image.jpg', 'rb')}
headers = {
    'X-Naver-Client-Id': Client ID,
    'X-Naver-Client-Secret': Client Secret
}

response = requests.post(url, headers=headers, files=files)
rescode = response.status_code

if rescode == 200:
    print(response.text)
else:
    print("Error Code:" + str(rescode))
```

## 응답 데이터 필드 (Celebrity)

- `faces`: 분석된 얼굴들의 리스트
  - `celebrity`: 가장 많이 닮은 유명인 정보
    - `value`: 유명인 이름
    - `confidence`: 닮은 정도 (0~1)

## 응답 데이터 필드 (Face)

- `faces`: 분석된 얼굴들의 리스트
  - `roi`: 얼굴 영역 (x, y, width, height)
  - `emotion`: 감정 (value, confidence)
  - `gender`: 성별 (value, confidence)
  - `age`: 추정 나이 (value, confidence)
  - `pose`: 얼굴 방향/기울기

## 오류 코드 가이드 가이드

| 상태 코드 | 상세 설명 |
| :--- | :--- |
| 400 | Bad Request (이미지 파일이 전송되지 않음 등) |
| 401 | Authentication Failed (ID/Secret 인증 실패) |
| 403 | Forbidden (API 신청 안 됨 혹은 한도 초가) |
| 413 | Payload Too Large (이미지 파일이 2MB를 초과함) |
| 500 | Internal Server Error (서버 장애) |

## 개발 시 유의 사항

- **이미지 규격**: 파일 용량은 최대 2MB이며, 정면 얼굴이 선명하게 나온 사진일수록 분석 정확도가 높아집니다.
- **개인정보**: 사용자의 얼굴 데이터는 민감한 개인정보이므로, 수집 및 전송 시 반드시 보안 정책을 준수해야 합니다.
- **멀티파트 전송**: REST API 호출 시 반드시 `multipart/form-data` 형식을 사용해야 파일이 정상적으로 전송됩니다.

## FAQ

- **Q: 한 이미지에 여러 얼굴이 있으면 어떻게 되나요?**
  - A: 인식된 모든 얼굴에 대해 각각의 분석 결과가 리스트 형태로 반환됩니다.
- **Q: 동물 얼굴도 인식이 되나요?**
  - A: 본 API는 사람의 얼굴을 모델로 훈련되었으므로 동물 얼굴 인식률은 낮을 수 있습니다.
