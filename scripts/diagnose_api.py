import asyncio
import os
import json
from kr_data_portal.financial_services import FinancialClient

async def main():
    # Attempting to find a key or using a known test pattern
    service_key = os.environ.get("DATA_PORTAL_SERVICE_KEY", "UNSET")
    
    print(f"--- API Diagnosis Start ---")
    print(f"Service Key Status: {'SET' if service_key != 'UNSET' else 'UNSET'}")
    
    async with FinancialClient(service_key=service_key) as client:
        params = {
            "basDt": "20260205",
            "itmsNm": "삼성전자"
        }
        print(f"Request Params: {params}")
        
        try:
            # Calling the method that now has the updated _request logic
            # We don't use .model_validate here yet to see the raw dict/error
            data = await client._request(
                "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo",
                params={**params, "resultType": "json"}
            )
            
            print(f"Raw Response Body (first 1000 chars):")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
            
            if "error" in data:
                print(f"\n[ERROR DETECTED]: {data['error']}")
                if "content" in data:
                    print(f"Error Content: {data['content']}")
            elif "response" in data:
                header = data["response"].get("header", {})
                print(f"\nAPI Header: {header}")
                
                body = data["response"].get("body", {})
                items = body.get("items", {})
                if items and "item" in items:
                    stock_items = items["item"]
                    print(f"\nFound {len(stock_items)} items.")
                    for idx, item in enumerate(stock_items):
                        print(f"Item {idx+1}: {item.get('itmsNm')} | Closing: {item.get('clpr')} | Date: {item.get('basDt')}")
                else:
                    print("\nNo items found in response body.")
                    
        except Exception as e:
            print(f"\n[EXCEPTION]: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
