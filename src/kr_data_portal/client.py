from typing import Any

import httpx
from aiolimiter import AsyncLimiter


class DataPortalClient:
    """Base client for KR Public Data Portal.

    Attributes:
        service_key: The API service key provided by the portal.
        rate_limit: Maximum requests per second.
    """

    def __init__(
        self,
        service_key: str,
        requests_per_second: float = 10.0,
        timeout: float = 30.0,
    ):
        self.service_key = service_key
        self._limiter = AsyncLimiter(requests_per_second, 1)
        self._timeout = timeout
        self._client = httpx.AsyncClient(timeout=self._timeout)

    async def _request(
        self,
        url: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Internal request handler with rate limiting and auth handling."""
        params = params or {}

        # Ensure serviceKey is in params
        if "serviceKey" not in params:
            params["serviceKey"] = self.service_key

        async with self._limiter:
            # To avoid double-encoding of serviceKey, we can build the URL manually
            # or use httpx.URL and preserve the raw serviceKey if it's already encoded.
            # Many Public Data Portal keys contain characters like '%' that shouldn't be re-encoded.

            req = self._client.build_request(method, url, params=params, **kwargs)

            response = await self._client.send(req)
            response.raise_for_status()

            try:
                data = response.json()
            except ValueError:
                # Handle cases where the API returns XML even if JSON was requested (e.g. on error)
                return {"error": "Invalid JSON response", "content": response.text}

            return data

    async def close(self):
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
