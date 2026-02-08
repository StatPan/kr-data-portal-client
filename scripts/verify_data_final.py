import os
import json
import requests
from dotenv import load_dotenv

def verify_data():
    # 1. Load environment variables
    load_dotenv()
    service_key = os.getenv("DATA_PORTAL_SERVICE_KEY")
    
    if not service_key:
        print("Error: DATA_PORTAL_SERVICE_KEY not found in .env file.")
        return

    # API Endpoint: Get Stock Price Info
    url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
    
    # Parameters for Samsung Electronics (005930) on 2026-02-05
    params = {
        "serviceKey": service_key,
        "numOfRows": "1",
        "pageNo": "1",
        "resultType": "json",
        "basDt": "20260205",
        "likeItmsNm": "삼성전자"
    }

    print(f"Requesting URL: {url}")
    print(f"Parameters: {params}")

    try:
        # 2. Call the API
        response = requests.get(url, params=params, timeout=10)
        
        # Save raw response
        with open("response_raw.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        print("\n--- Raw Response Body ---")
        print(response.text)
        print("-------------------------\n")

        # 3. Parse JSON and extract clpr
        data = response.json()
        
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        
        if not items:
            print("No data found for the given parameters.")
            return

        item = items[0]
        clpr = item.get("clpr")
        itmsNm = item.get("itmsNm")
        basDt = item.get("basDt")

        print(f"Result Confirmation:")
        print(f"- Item Name: {itmsNm}")
        print(f"- Base Date: {basDt}")
        print(f"- Closing Price (clpr): {clpr}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    verify_data()
