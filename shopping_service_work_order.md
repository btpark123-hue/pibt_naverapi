# 웹서비스 작업지시서: 쇼핑 트렌드 인사이트 대시보드

## 1. 프로젝트 개요

- **프로젝트명**: 네이버 쇼핑 트렌드 수집 및 분석 서비스
- **목표**: 네이버 데이터랩 쇼핑인사이트 API를 활용하여 지난 1년간의 일자별 쇼핑 트렌드 데이터를 수집하고, 이를 시각적으로 확인할 수 있는 프리미엄 웹 대시보드를 구축함.
- **주요 사용자**: 이커머스 셀러, 마케팅 전략 수립자, 데이터 분석가.

## 2. 주요 기능 요구사항

### 2.1 데이터 수집 및 관리 (Backend)

- **API 연동**: [쇼핑인사이트 API](file:///c:/naver_api/docs/datalab_shopping.md)를 사용하여 카테고리별 클릭 추이 데이터를 수집함.
- **수집 범위**: 현재 날짜 기준 과거 1년(365일) 간의 데이터를 일 단위(`timeUnit: 'date'`)로 수집.
- **자동화**: 스케줄러를 구현하여 매일 오전 네이버의 데이터 업데이트 주기에 맞춰 신규 데이터를 자동 업데이트함.
- **데이터베이스**: 수집된 상대 수치(Ratio)를 저장하여 과거 트렌드를 실시간 호출 없이 즉시 조회 가능하도록 최적화.

### 2.2 사용자 인터페이스 (Frontend)

- **데이터 시각화**: Chart.js 또는 Recharts를 활용하여 1년간의 추이를 한눈에 볼 수 있는 인터랙티브 라인 차트 구현.
- **필터링 옵션**:
  - **카테고리**: 패션잡화, 가전/디지털 등 대분류 선택 가능.
  - **세부 타겟**: 성별(남/여), 연령대(10~60대), 기기(PC/모바일) 필터 적용.
- **디자인 컨셉**:
  - **Rich Aesthetics**: 다크 모드 기반의 세련된 컬러 팔레트 사용.
  - **Glassmorphism**: 투명도와 블러 효과를 활용한 카드 UI 레이아웃.
  - **Micro-animations**: 차트 로딩 및 호버 시 부드러운 애니메이션 효과 적용.

## 3. 기술 스택 제안

- **Frontend**: React.js / Vite (빠른 응답성 및 컴포넌트 기반 개발)
- **Backend**: Node.js (Express) 또는 Python (FastAPI) - [API 예제 참조](file:///c:/naver_api/docs/datalab_shopping.md#%EA%B5%AC%ED%98%84-%EC%98%88%EC%A0%9C-java)
- **Styling**: Vanilla CSS 또는 Tailwind CSS (프리미엄 UI 구현용)

## 4. 개발 단계별 상세 공정

### 1단계: 환경 설정 및 API 인증

- [애플리케이션 등록 가이드](file:///c:/naver_api/docs/appregister.md)에 따라 Client ID 및 Client Secret 발급 및 환경 변수 설정.

### 2단계: 데이터 수집 엔진 개발

- 과거 1년치 데이터를 csv파일로 data폴더에 저장하여 관리.
- 에러 발생 시 재시도 로직 구현.

### 3단계: 대시보드 UI 개발

- 메인 차트 및 필터 UI 구성.
- 사용자가 카테고리를 변경할 때마다 실시간으로 csv에서 데이터를 불러와 차트 갱신.

## 5. 관련 참고 문서

- **인증 가이드**: [appregister.md](file:///c:/naver_api/docs/appregister.md)
- **쇼핑 API 상세**: [datalab_shopping.md](file:///c:/naver_api/docs/datalab_shopping.md)
- **공통 오류 코드**: [apilist_nonlogin.md](file:///c:/naver_api/docs/apilist_nonlogin.md#%EC%98%A4%EB%A5%98-%EC%BD%94%EB%93%9C-%EA%B0%80%EC%9D%B4%EB%93%9C-common-errors)

---
*본 작업지시서는 수집된 네이버 API 가이드를 바탕으로 작성되었습니다.*
