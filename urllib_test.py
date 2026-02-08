
import urllib.parse
import urllib.request
import json
import time

def call_api(service_key, bas_dt, itms_nm, label):
    base_url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
    
    # 공공데이터포털의 악명높은 인증키 이슈 해결을 위한 매뉴얼 쿼리 스트링 구성
    # itmsNm만 안전하게 인코딩하고, serviceKey는 받은 그대로 붙임
    safe_item = urllib.parse.quote(itms_nm)
    query = f"?serviceKey={service_key}&numOfRows=1&pageNo=1&resultType=json&basDt={bas_dt}&itmsNm={safe_item}"
    full_url = base_url + query
    
    print(f"[{label}] 🔍 {itms_nm} 요청 중...")
    
    req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
            if "Forbidden" in content:
                print(f"   ❌ Forbidden 에러 발생")
                return None
            
            try:
                data = json.loads(content)
                items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                if items:
                    item_data = items[0]
                    print(f"   ✅ 성공! 종가: {item_data.get('clpr')}원 (대비 {item_data.get('vs')})")
                    return item_data
                else:
                    print(f"   ⚠️ 데이터가 없습니다. (결과 내용: {content[:100]})")
            except:
                print(f"   ❌ JSON 파싱 실패 (결과 내용: {content[:100]})")
    except Exception as e:
        print(f"   ❌ 요청 실패: {e}")
    return None

def main():
    # 교수님이 주신 키들
    encoded_key = "lF2Troovy8WHzmjjGoOMyg7BPNXTkeri0%2F%2FATEYGBnEtQCSbdBmfB0SrE4gEHzAANPs5pegxILESomSg8kKCPQ%3D%3D"
    decoded_key = "lF2Troovy8WHzmjjGoOMyg7BPNXTkeri0//ATEYGBnEtQCSbdBmfB0SrE4gEHzAANPs5pegxILESomSg8kKCPQ=="
    
    bas_dt = "20260206"
    targets = ["삼성전자", "SK하이닉스"]
    
    for label, key in [("ENCODED", encoded_key), ("DECODED", decoded_key)]:
        print(f"\n--- {label} KEY VARIATION TEST ---")
        for stock in targets:
            call_api(key, bas_dt, stock, label)
            time.sleep(1) # 간격 두기

if __name__ == "__main__":
    main()
