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

## 주요 API 서비스

본 라이브러리는 현재 금융위원회 주식시세정보의 4개 핵심 API를 지원합니다:

1.  **`get_stock_price_info`**: 상장 주식의 일별 시세 (종가, 대비, 거래량 등)
2.  **`get_securities_price_info`**: 수익증권(ETF, ETN, 리츠 등)의 시세
3.  **`get_preemptive_right_certificate_price_info`**: 신주인수권증서의 시세 (유상증자 이벤트 트래킹용)
4.  **`get_preemptive_right_warrant_price_info`**: 신주인수권증권(워런트)의 시세

## 사용 예시

모든 API 메서드는 공공데이터포털의 파라미터를 **가변 키워드 인자(`**kwargs`)**로 유연하게 받습니다. 필요한 파라미터만 선택적으로 전달하세요.

```python
import asyncio
from kr_data_portal import DataPortalClient

async def main():
    async with DataPortalClient() as client:
        # 1. 주식 시세 조회 (종목명으로 필터링)
        stock = await client.get_stock_price_info(
            basDt="20260205",
            itmsNm="삼성전자"
        )
        
        # 2. 신주인수권증서 조회 (페이징 적용)
        rights = await client.get_preemptive_right_certificate_price_info(
            basDt="20260205",
            numOfRows=100,
            pageNo=1
        )
        
        # 3. 특정 시장(KOSPI) 전체 조회
        kospi_today = await client.get_stock_price_info(
            basDt="20260205",
            mrktCtg="KOSPI"
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## 주요 파라미터 (Optional)
각 메서드는 공공데이터포털 가이드의 모든 파라미터를 지원합니다:
- `basDt`: 기준일자 (YYYYMMDD)
- `itmsNm`: 종목명 (완전일치)
- `mrktCtg`: 시장구분 (KOSPI/KOSDAQ/KONEX)
- `numOfRows`: 페이지당 결과 수
- `pageNo`: 페이지 번호
- `isinCd`: ISIN 코드 등

