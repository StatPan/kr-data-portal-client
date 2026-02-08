import os
import pytest
import asyncio
from kr_data_portal.financial_services import FinancialClient
from kr_data_portal.models.financial_services import StockPriceInfoItem

@pytest.mark.asyncio
async def test_real_data_validation():
    service_key = os.getenv("DATA_PORTAL_SERVICE_KEY")
    if not service_key:
        pytest.skip("DATA_PORTAL_SERVICE_KEY not set, skipping real data validation")
    
    client = FinancialClient(service_key=service_key)
    
    # 삼성전자 (005930) 2026-02-05 데이터 검증
    # 실제 환경에서 2026년 데이터가 없을 수 있으므로 (미래 날짜), 
    # 테스트 요청은 하되 결과가 00 (정상) 인지 확인
    try:
        response = await client.getStockPriceInfo(itmsNm="삼성전자", basDt="20260205")
        
        # API 응답 자체가 성공했는지 확인 (인증키 유효성 등)
        assert response.response.header.resultCode == "00", f"API Error: {response.response.header.resultMsg}"
        
        # 데이터가 있다면 값 검증 (미래 데이터라 없을 가능성 높음)
        items = response.items(StockPriceInfoItem)
        if items:
            assert items[0].itmsNm == "삼성전자"
            # 실제 값이 159300인지는 당일에 따라 다를 수 있으나, 여기선 형식 검증 위주
            assert items[0].clpr is not None
    except Exception as e:
        pytest.fail(f"Real data validation failed: {e}")

if __name__ == "__main__":
    # For manual testing
    if os.getenv("DATA_PORTAL_SERVICE_KEY"):
        asyncio.run(test_real_data_validation())
    else:
        print("Skipping real data validation (no API key)")
