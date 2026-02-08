
import asyncio
import httpx
import json
import urllib.parse
from client import StockPriceClient

async def test_key_variations():
    # 교수님이 주신 키들
    encoded_key = "lF2Troovy8WHzmjjGoOMyg7BPNXTkeri0%2F%2FATEYGBnEtQCSbdBmfB0SrE4gEHzAANPs5pegxILESomSg8kKCPQ%3D%3D"
    decoded_key = "lF2Troovy8WHzmjjGoOMyg7BPNXTkeri0//ATEYGBnEtQCSbdBmfB0SrE4gEHzAANPs5pegxILESomSg8kKCPQ=="
    
    bas_dt = "20260206"
    items = ["삼성전자", "SK하이닉스"]
    
    # 공공데이터포털은 종종 인코딩된 키를 '그대로' 쏴야할 때가 있고, 
    # 디코딩된 키를 '라이브러리가 인코딩하게' 둬야할 때가 있습니다.
    variations = [
        ("ENCODED_KEY_RAW", encoded_key),
        ("DECODED_KEY_RAW", decoded_key),
    ]

    print(f"🌿 인증키 바리에이션 테스트 시작 (대상 일자: {bas_dt})")
    
    for label, key in variations:
        print(f"\n--- Testing with {label} ---")
        async with StockPriceClient(service_key=key) as client:
            for item in items:
                print(f"🔍 {item} 조회 중...", end=" ", flush=True)
                # itmsNm은 한글이므로 안전하게 인코딩
                safe_item = urllib.parse.quote(item)
                result = await client.get_stock_price_info(basDt=bas_dt, itmsNm=safe_item)
                
                if isinstance(result, dict) and "error" in result:
                    print(f"❌ 실패: {result['error']}")
                    # print(f"   내용: {result['content'][:100]}...")
                else:
                    print(f"✅ 성공!")
                    # 성공 시 첫 번째 아이템의 시세 출력
                    try:
                        item_data = result.get('response', {}).get('body', {}).get('items', {}).get('item', [])[0]
                        print(f"   [결과] 종가: {item_data.get('clpr')}원 / 대비: {item_data.get('vs')} / 등락률: {item_data.get('fltRt')}%")
                    except Exception as e:
                        print(f"   데이터 추출 실패: {e}")

if __name__ == "__main__":
    # httpx를 임시로 설치 (없을 경우를 대비해 스크립트 내에서 에러 처리)
    try:
        asyncio.run(test_key_variations())
    except ImportError:
        print("❌ httpx 라이브러리가 필요합니다. 'pip install httpx'를 실행해주세요.")
