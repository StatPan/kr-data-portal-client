from typing import Any
import httpx
from aiolimiter import AsyncLimiter

class DataPortalError(Exception):
    """Base exception for KR Data Portal Client."""
    def __init__(self, message: str, code: str = None, response: httpx.Response = None):
        self.message = message
        self.code = code
        self.response = response
        super().__init__(self.message)

class ServiceError(DataPortalError):
    """Exception for API-level errors (e.g., SERVICE_TIMEOUT, INVALID_SERVICE_KEY)."""
    pass

class DataPortalClient:
    """Base client for KR Public Data Portal.

    Attributes:
        service_key: The API service key provided by the portal.
        rate_limit: Maximum requests per second.
        use_retry: Whether to use automatic retries.
        max_retries: Maximum number of retries if use_retry is True.
    """

    def __init__(
        self,
        service_key: str,
        requests_per_second: float = 10.0,
        timeout: float = 30.0,
        use_retry: bool = False,
        max_retries: int = 3,
    ):
        self.service_key = service_key
        self._limiter = AsyncLimiter(requests_per_second, 1)
        self._timeout = timeout
        self._client = httpx.AsyncClient(timeout=self._timeout)
        self._use_retry = use_retry
        self._max_retries = max_retries

    async def _request(
        self,
        url: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Internal request handler with rate limiting and auth handling."""
        params = params or {}

        # URL validation: Ensure https
        if url.startswith("http://"):
            url = url.replace("http://", "https://", 1)

        # Ensure serviceKey is in params
        if "serviceKey" not in params:
            params["serviceKey"] = self.service_key

        async with self._limiter:
            # Manual URL construction to prevent double-encoding of serviceKey
            base_url = httpx.URL(url)
            
            # Extract serviceKey to handle it separately
            key = params.pop("serviceKey")
            
            # Build query string
            query_parts = []
            for k, v in params.items():
                query_parts.append(f"{k}={v}")
            
            # Append raw serviceKey
            query_string = "&".join(query_parts)
            if query_string:
                final_url = f"{url}?{query_string}&serviceKey={key}"
            else:
                final_url = f"{url}?serviceKey={key}"

            if self._use_retry:
                # Basic retry logic using httpx.AsyncRetrying style if needed, 
                # but simple implementation for clarity
                attempt = 0
                while attempt <= self._max_retries:
                    try:
                        response = await self._client.request(method, final_url, **kwargs)
                        return self._handle_response(response)
                    except (httpx.RequestError, ServiceError) as e:
                        attempt += 1
                        if attempt > self._max_retries:
                            raise e
                        # Optional: Add small delay or exponential backoff
            else:
                response = await self._client.request(method, final_url, **kwargs)
                return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Validate response and check for service-level errors."""
        if response.status_code != 200:
            raise DataPortalError(f"HTTP {response.status_code}: {response.text}", response=response)

        # Check for error messages in body even if 200 OK
        content = response.text
        
        # Check for XML error messages (common in Korean Public Data Portal)
        if "<returnAuthMsg>" in content or "<cmmMsgHeader>" in content:
            # Simple extraction for common error patterns
            import re
            msg_match = re.search(r"<(returnAuthMsg|errMsg)>(.*?)</\1>", content)
            code_match = re.search(r"<(returnReasonCode|returnCode)>(.*?)</\1>", content)
            
            msg = msg_match.group(2) if msg_match else "Unknown Service Error"
            code = code_match.group(2) if code_match else "UNKNOWN"
            
            raise ServiceError(f"API Error ({code}): {msg}", code=code, response=response)

        try:
            data = response.json()
            
            # Check for JSON error patterns
            # Standard response structure: {"response": {"header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE"}}}
            if isinstance(data, dict) and "response" in data:
                header = data["response"].get("header", {})
                code = header.get("resultCode", "00")
                msg = header.get("resultMsg", "")
                
                if code != "00":
                    raise ServiceError(f"API Error ({code}): {msg}", code=code, response=response)
            
            return data
        except ValueError:
            # If not JSON, it might be an unhandled XML error or garbage
            if "<errMsg>" in content or "SERVICE_TIMEOUT" in content:
                raise ServiceError(f"Service Error Detected: {content}", response=response)
            raise DataPortalError("Invalid JSON response and not recognized XML error", response=response)

    async def close(self):
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
