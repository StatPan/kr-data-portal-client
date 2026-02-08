from unittest.mock import AsyncMock, patch

import pytest
from kr_data_portal.client import DataPortalClient


@pytest.mark.asyncio
async def test_get_stock_price_info_mock():
    # Mocking httpx response
    mock_response = {
        "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."},
            "body": {
                "numOfRows": 1,
                "pageNo": 1,
                "totalCount": 1,
                "items": {"item": [{"basDt": "20260205", "itmsNm": "삼성전자", "clpr": "150000"}]},
            },
        }
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        async with DataPortalClient(service_key="test_key") as client:
            result = await client.get_stock_price_info(basDt="20260205", itmsNm="삼성전자")
            assert result.response.header.resultCode == "00"
            assert result.response.body.items["item"][0]["itmsNm"] == "삼성전자"
