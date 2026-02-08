# kr-data-portal-client (South Korea Public Data Portal Client)

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

공공데이터포털(data.go.kr)의 다양한 API를 통합적으로 관리하고 호출하기 위한 비동기 Python 클라이언트 라이브러리입니다. `StatPan` 시리즈 API 클라이언트의 설계를 계승합니다.

## 특징
- ✨ **비동기 우선**: `asyncio`와 `httpx` 기반 고성능 비동기 요청
- 🔒 **타입 안전성**: Pydantic 모델과 타입 힌트로 IDE 자동완성 지원
- 🚀 **시리즈 일관성**: `dart-api-client`, `assembly-api-client`와 동일한 사용 경험 제공
- ⚡ **Rate Limiting**: 클라이언트 측 요청 제한으로 공공데이터포털 API 가이드 준수
- 📝 **스케줄링 힌트**: 각 메서드에 데이터 갱신 주기 및 업데이트 시각 정보 포함 (Airflow 최적화)

## 패키지 구조
- `src/client.py`: 공용 API 통신 클라이언트
- `src/services/financial/stock.py`: 금융위 주식시세 API 특화 로직
- `requirements.txt`: 필요한 의존성 라이브러리

## API Spec (금융위 주식시세정보)
- **Base URL**: http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService
- **Endpoints**:
  - `getStockPriceInfo`: 주식시세정보 조회
- **Key Params**:
  - `serviceKey`: 인증키
  - `basDt`: 기준일자 (YYYYMMDD)
  - `itmsNm`: 종목명
  - `numOfRows`, `pageNo`: 페이징
