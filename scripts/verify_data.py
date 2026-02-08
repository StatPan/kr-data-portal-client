import asyncio
import os
from kr_data_portal.financial_services import FinancialClient

async def main():
    # Use the service key from environment variable or placeholder
    service_key = os.environ.get("DATA_PORTAL_SERVICE_KEY", "YOUR_SERVICE_KEY")
    if service_key == "YOUR_SERVICE_KEY":
        print("Error: DATA_PORTAL_SERVICE_KEY environment variable not set.")
        return

    async with FinancialClient(service_key=service_key) as client:
        # 2026-02-05 삼성전자 (Samsung Electronics) 주가 조회
        # 삼성전자 종목코드: 005930
        print("Fetching Samsung Electronics stock price for 2026-02-05...")
        response = await client.getStockPriceInfo(
            basDt="20260205",
            itmsNm="삼성전자"
        )
        
        if response.body.items:
            for item in response.body.items:
                print(f"Date: {item.basDt}")
                print(f"Item: {item.itmsNm}")
                print(f"Closing Price: {item.clpr}")
                print(f"High: {item.hipr}")
                print(f"Low: {item.lopr}")
                print(f"Open: {item.mkp}")
        else:
            print("No data found for the given criteria.")

if __name__ == "__main__":
    asyncio.run(main())
