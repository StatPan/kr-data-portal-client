from unittest.mock import AsyncMock, patch

import pytest

from kr_data_portal.financial_services import FinancialClient
from kr_data_portal.models.base import DataPortalResponse
from kr_data_portal.models.financial_services import (
    DerivativesPriceInfoItem,
    EtfPriceInfoItem,
    EtnPriceInfoItem,
    StockPriceInfoItem,
)


@pytest.fixture
def mock_client():
    return FinancialClient(service_key="test_key")


@pytest.mark.asyncio
async def test_get_stock_price_info(mock_client):
    mock_response = {
        "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."},
            "body": {
                "items": {"item": [{"itmsNm": "삼성전자", "clpr": "70000"}]},
                "numOfRows": 10,
                "pageNo": 1,
                "totalCount": 1,
            },
        }
    }

    with patch.object(mock_client, "_request", new_callable=AsyncMock) as mock_req:
        mock_req.return_value = mock_response

        response = await mock_client.getStockPriceInfo(itmsNm="삼성전자")

        assert isinstance(response, DataPortalResponse)
        assert response.response.header.resultCode == "00"
        items = response.items(StockPriceInfoItem)
        assert len(items) == 1
        assert items[0].itmsNm == "삼성전자"
        assert items[0].clpr == "70000"


@pytest.mark.asyncio
async def test_get_etf_price_info(mock_client):
    mock_response = {
        "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."},
            "body": {
                "items": {"item": [{"itmsNm": "KODEX 200", "clpr": "30000"}]},
                "numOfRows": 10,
                "pageNo": 1,
                "totalCount": 1,
            },
        }
    }

    with patch.object(mock_client, "_request", new_callable=AsyncMock) as mock_req:
        mock_req.return_value = mock_response

        response = await mock_client.getEtfPriceInfo(itmsNm="KODEX 200")

        assert response.response.header.resultCode == "00"
        items = response.items(EtfPriceInfoItem)
        assert items[0].itmsNm == "KODEX 200"


@pytest.mark.asyncio
async def test_get_etn_price_info(mock_client):
    mock_response = {
        "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."},
            "body": {
                "items": {"item": [{"itmsNm": "ETN ITEM", "clpr": "10000"}]},
                "numOfRows": 10,
                "pageNo": 1,
                "totalCount": 1,
            },
        }
    }

    with patch.object(mock_client, "_request", new_callable=AsyncMock) as mock_req:
        mock_req.return_value = mock_response

        response = await mock_client.getEtnPriceInfo(itmsNm="ETN ITEM")

        assert response.response.header.resultCode == "00"
        items = response.items(EtnPriceInfoItem)
        assert items[0].itmsNm == "ETN ITEM"


@pytest.mark.asyncio
async def test_get_derivatives_price_info(mock_client):
    mock_response = {
        "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."},
            "body": {
                "items": {"item": [{"itmsNm": "FUTURES", "clpr": "400"}]},
                "numOfRows": 10,
                "pageNo": 1,
                "totalCount": 1,
            },
        }
    }

    with patch.object(mock_client, "_request", new_callable=AsyncMock) as mock_req:
        mock_req.return_value = mock_response

        response = await mock_client.getDerivativesPriceInfo(itmsNm="FUTURES")

        assert response.response.header.resultCode == "00"
        items = response.items(DerivativesPriceInfoItem)
        assert items[0].itmsNm == "FUTURES"
