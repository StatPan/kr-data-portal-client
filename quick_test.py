
import httpx
import asyncio
import json
from typing import Optional

async def fetch_stock_price(service_key: str, bas_dt: str, itms_nm: str):
    url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
    params = {
        "serviceKey": service_key,
        "numOfRows": 1,
        "pageNo": 1,
        "resultType": "json",
        "basDt": bas_dt,
        "itmsNm": itms_nm
    }
    
    async with httpx.AsyncClient() as client:
        # Note: Public Data Portal often requires the UNENCODED key because httpx/requests will encode it again.
        # But sometimes it needs the raw string. We'll use the decoding key as it's usually safer with params.
        response = await client.get(url, params=params, timeout=30.0)
        return response.json()

async def main():
    service_key = "lF2Troovy8WHzmjjGoOMyg7BPNXTkeri0//ATEYGBnEtQCSbdBmfB0SrE4gEHzAANPs5pegxILESomSg8kKCPQ=="
    bas_dt = "20260206"
    
    print(f"🌿 2026-02-06 주식 시세 호출 시작...")
    
    # 삼성전자
    samsung = await fetch_stock_price(service_key, bas_dt, "삼성전자")
    print(f"\n[삼성전자 결과]")
    print(json.dumps(samsung, indent=2, ensure_ascii=False))
    
    # SK하이닉스
    hynix = await fetch_stock_price(service_key, bas_dt, "SK하이닉스")
    print(f"\n[SK하이닉스 결과]")
    print(json.dumps(hynix, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
