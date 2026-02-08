import httpx
import asyncio
import yaml
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from pydantic import BaseModel
from pathlib import Path

from .models import BaseApiResponse, StockPriceItem

T = TypeVar("T")

class RateLimiter:
    """Simple rate limiter to comply with API usage limits."""
    def __init__(self, requests_per_second: float = 2.0):
        self.delay = 1.0 / requests_per_second
        self._last_call = 0.0
        self._lock = asyncio.Lock()

    async def wait(self):
        async with self._lock:
            current_time = asyncio.get_event_loop().time()
            elapsed = current_time - self._last_call
            if elapsed < self.delay:
                await asyncio.sleep(self.delay - elapsed)
            self._last_call = asyncio.get_event_loop().time()

class StockPriceClient:
    """
    Python client for Financial Services Commission - Stock Price Information.
    
    Data Policy & Update Rules:
    - Refresh Cycle: Daily (1 per day)
    - Update Timing: After 13:00 (1 PM) on the next business day.
      (e.g., Friday's data is updated on Monday after 13:00).
    - Airflow Scheduling Hint: '0 14 * * 1-5' (2 PM KST on weekdays)
    """

    def __init__(self, service_key: str, rate_limit: float = 2.0):
        self.service_key = service_key
        self.base_url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService"
        self.client = httpx.AsyncClient(timeout=30.0)
        self.limiter = RateLimiter(rate_limit)
        self._spec = self._load_spec()

    def _load_spec(self) -> Dict[str, Any]:
        spec_path = Path(__file__).parent / "specs" / "financial_services.yaml"
        if spec_path.exists():
            with open(spec_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    async def _get(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        await self.limiter.wait()
        
        # Public Data Portal is notorious for ServiceKey encoding issues.
        # We'll try to pass it as a raw string to avoid double encoding by httpx.
        request_params = params.copy()
        if "resultType" not in request_params:
            request_params["resultType"] = "json"

        # Construct the URL manually to ensure the ServiceKey is handled exactly as provided
        # Some endpoints only work with the ENCODED key, others with the DECODED key.
        # We append it manually to the URL to bypass httpx's automatic param encoding for this specific key.
        base_query = f"?serviceKey={self.service_key}"
        for k, v in request_params.items():
            base_query += f"&{k}={v}"
            
        full_url = f"{self.base_url}{endpoint}{base_query}"
        
        # We use a custom call without params dict to prevent re-encoding
        response = await self.client.get(full_url)
        
        # If the response is XML despite resultType=json (happens on errors), 
        # or if we get a Forbidden, we'll need to report it.
        if response.status_code != 200:
             return {"error": f"HTTP {response.status_code}", "content": response.text}
             
        try:
            return response.json()
        except:
            return {"error": "JSON parse failed", "content": response.text}


    async def get_stock_price_info(self, **kwargs) -> BaseApiResponse[StockPriceItem]:
        """
        주식 시세 정보를 조회합니다. (getStockPriceInfo)
        
        Refresh Cycle: Daily
        Update Timing: T+1 13:00 KST
        """
        data = await self._get("/getStockPriceInfo", kwargs)
        return BaseApiResponse[StockPriceItem](**data)

    async def get_beneficiary_certificate_price_info(self, **kwargs) -> BaseApiResponse[Any]:
        """
        수익증권 시세 정보를 조회합니다. (getBeneficiaryCertificatePriceInfo)
        
        Refresh Cycle: Daily
        Update Timing: T+1 13:00 KST
        """
        data = await self._get("/getBeneficiaryCertificatePriceInfo", kwargs)
        return BaseApiResponse[Any](**data)

    async def get_preemptive_right_certificate_price_info(self, **kwargs) -> BaseApiResponse[Any]:
        """
        신주인수권증권 시세 정보를 조회합니다. (getPreemptiveRightCertificatePriceInfo)
        
        Refresh Cycle: Daily
        Update Timing: T+1 13:00 KST
        """
        data = await self._get("/getPreemptiveRightCertificatePriceInfo", kwargs)
        return BaseApiResponse[Any](**data)

    async def get_preemptive_right_warrant_price_info(self, **kwargs) -> BaseApiResponse[Any]:
        """
        신주인수권증서 시세 정보를 조회합니다. (getPreemptiveRightWarrantPriceInfo)
        
        Refresh Cycle: Daily
        Update Timing: T+1 13:00 KST
        """
        data = await self._get("/getPreemptiveRightWarrantPriceInfo", kwargs)
        return BaseApiResponse[Any](**data)

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
