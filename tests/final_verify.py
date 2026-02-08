
import asyncio
import httpx
import json
import urllib.parse
from client import StockPriceClient

async def final_verify():
    # 교수님이 주신 인코딩된 키
    service_key = "lF2Troovy8WHzmjjGoOMyg7BPNXTkeri0%2F%2FATEYGBnEtQCSbdBmfB0SrE4gEHzAANPs5pegxILESomSg8kKCPQ%3D%3D"
    
    # 데이터가 확실히 존재하는 날짜 (2026-02-05 목요일)
    bas_dt = "20260205"
    
    print(f"🚀 [최종 검증] 4개 API 실서버 호출 테스트 시작 (기준일: {bas_dt})")
    
    # itmsNm 인코딩을 클라이언트가 어떻게 처리하는지 확인하며 진행
    async with StockPriceClient(service_key=service_key) as client:
        # 1. 주식시세 (getStockPriceInfo)
        print("1. 주식시세 조회 중...", end=" ", flush=True)
        # 클라이언트 내부에서 manually 구성하므로 itmsNm은 여기서 인코딩해서 넘김
        safe_nm = urllib.parse.quote("삼성전자")
        stock = await client.get_stock_price_info(basDt=bas_dt, itmsNm=safe_nm, numOfRows=1)
        
        if isinstance(stock, dict) and "error" in stock:
             print(f"❌ 실패 ({stock['error']})")
        elif stock.response.header.resultCode == "00":
            count = stock.response.body.totalCount
            if count > 0:
                print(f"✅ 성공 (삼성전자 종가: {stock.response.body.items['item'][0]['clpr']})")
            else:
                print(f"⚠️ 성공했으나 데이터 없음")
        else:
            print(f"❌ 실패 ({stock.response.header.resultMsg})")

        # 2. 수익증권시세 (getBeneficiaryCertificatePriceInfo)
        print("2. 수익증권시세 조회 중...", end=" ", flush=True)
        securities = await client.get_beneficiary_certificate_price_info(basDt=bas_dt, numOfRows=1)
        if isinstance(securities, dict) and "error" in securities:
             print(f"❌ 실패 ({securities['error']})")
        elif securities.response.header.resultCode == "00":
            print(f"✅ 성공 (데이터 수: {securities.response.body.totalCount})")
        else:
            print(f"❌ 실패 ({securities.response.header.resultMsg})")

        # 3. 신주인수권증권시세 (getPreemptiveRightSecuritiesPriceInfo)
        print("3. 신주인수권증권시세 조회 중...", end=" ", flush=True)
        # 메서드명이 YAML/client와 일치하는지 확인 (get_preemptive_right_certificate_price_info 가 신주인수권증권)
        rights_sec = await client.get_preemptive_right_certificate_price_info(basDt=bas_dt, numOfRows=1)
        if isinstance(rights_sec, dict) and "error" in rights_sec:
             print(f"❌ 실패 ({rights_sec['error']})")
        elif rights_sec.response.header.resultCode == "00":
            print(f"✅ 성공 (데이터 수: {rights_sec.response.body.totalCount})")
        else:
            print(f"❌ 실패 ({rights_sec.response.header.resultMsg})")

        # 4. 신주인수권증서시세 (getPreemptiveRightWarrantPriceInfo)
        print("4. 신주인수권증서시세 조회 중...", end=" ", flush=True)
        warrant = await client.get_preemptive_right_warrant_price_info(basDt=bas_dt, numOfRows=1)
        if isinstance(warrant, dict) and "error" in warrant:
             print(f"❌ 실패 ({warrant['error']})")
        elif warrant.response.header.resultCode == "00":
            print(f"✅ 성공 (데이터 수: {warrant.response.body.totalCount})")
        else:
            print(f"❌ 실패 ({warrant.response.header.resultMsg})")

if __name__ == "__main__":
    try:
        import httpx
        asyncio.run(final_verify())
    except ImportError:
        print("\n❌ httpx가 설치되지 않았습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
