from typing import Any

from .client import DataPortalClient
from .models.base import DataPortalResponse
from .models.financial_services import (
    DerivativesPriceInfoItem,
    EtfPriceInfoItem,
    EtnPriceInfoItem,
    StockPriceInfoItem,
)


class FinancialClient(DataPortalClient):
    """APIs for stock, ETF, ETN, and derivatives prices from FSC.

    Base URL: http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService
    """

    async def getStockPriceInfo(
        self,
        numOfRows: int = 10,
        pageNo: int = 1,
        basDt: str = None,
        itmsNm: str = None,
        crno: str = None,
        stckIssuItmsNm: str = None,
        **kwargs: Any,
    ) -> DataPortalResponse[StockPriceInfoItem]:
        """주식시세정보를 조회하는 서비스입니다.

        Data Update Policy:
        - Cycle: Daily
        - Timing: After market close (16:00 KST)

        Args:

            numOfRows (int): 한 페이지 결과 수

            pageNo (int): 페이지 번호

            basDt (str): 기준일자 (YYYYMMDD)

            itmsNm (str): 종목명

            crno (str): 법인등록번호

            stckIssuItmsNm (str): 주식발행종목명

            **kwargs: Additional request parameters.

        Returns:
            DataPortalResponse[StockPriceInfoItem]: The API response.
        """
        params = {
            "resultType": "json",
            "numOfRows": numOfRows,
            "pageNo": pageNo,
            "basDt": basDt,
            "itmsNm": itmsNm,
            "crno": crno,
            "stckIssuItmsNm": stckIssuItmsNm,
        }
        params.update(kwargs)

        data = await self._request(
            "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo",
            params={k: v for k, v in params.items() if v is not None},
        )
        return DataPortalResponse[StockPriceInfoItem].model_validate(data)

    async def getEtfPriceInfo(
        self,
        numOfRows: int = 10,
        pageNo: int = 1,
        basDt: str = None,
        itmsNm: str = None,
        **kwargs: Any,
    ) -> DataPortalResponse[EtfPriceInfoItem]:
        """ETF시세정보를 조회하는 서비스입니다.

        Data Update Policy:
        - Cycle: Daily
        - Timing: After market close (16:00 KST)

        Args:

            numOfRows (int): No description

            pageNo (int): No description

            basDt (str): No description

            itmsNm (str): No description

            **kwargs: Additional request parameters.

        Returns:
            DataPortalResponse[EtfPriceInfoItem]: The API response.
        """
        params = {
            "resultType": "json",
            "numOfRows": numOfRows,
            "pageNo": pageNo,
            "basDt": basDt,
            "itmsNm": itmsNm,
        }
        params.update(kwargs)

        data = await self._request(
            "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getGetEtfPriceInfo",
            params={k: v for k, v in params.items() if v is not None},
        )
        return DataPortalResponse[EtfPriceInfoItem].model_validate(data)

    async def getEtnPriceInfo(
        self,
        numOfRows: int = 10,
        pageNo: int = 1,
        basDt: str = None,
        itmsNm: str = None,
        **kwargs: Any,
    ) -> DataPortalResponse[EtnPriceInfoItem]:
        """ETN시세정보를 조회하는 서비스입니다.

        Data Update Policy:
        - Cycle: Daily
        - Timing: After market close (16:00 KST)

        Args:

            numOfRows (int): No description

            pageNo (int): No description

            basDt (str): No description

            itmsNm (str): No description

            **kwargs: Additional request parameters.

        Returns:
            DataPortalResponse[EtnPriceInfoItem]: The API response.
        """
        params = {
            "resultType": "json",
            "numOfRows": numOfRows,
            "pageNo": pageNo,
            "basDt": basDt,
            "itmsNm": itmsNm,
        }
        params.update(kwargs)

        data = await self._request(
            "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getGetEtnPriceInfo",
            params={k: v for k, v in params.items() if v is not None},
        )
        return DataPortalResponse[EtnPriceInfoItem].model_validate(data)

    async def getDerivativesPriceInfo(
        self,
        numOfRows: int = 10,
        pageNo: int = 1,
        basDt: str = None,
        itmsNm: str = None,
        **kwargs: Any,
    ) -> DataPortalResponse[DerivativesPriceInfoItem]:
        """파생상품시세정보를 조회하는 서비스입니다.

        Data Update Policy:
        - Cycle: Daily
        - Timing: After market close (16:00 KST)

        Args:

            numOfRows (int): No description

            pageNo (int): No description

            basDt (str): No description

            itmsNm (str): No description

            **kwargs: Additional request parameters.

        Returns:
            DataPortalResponse[DerivativesPriceInfoItem]: The API response.
        """
        params = {
            "resultType": "json",
            "numOfRows": numOfRows,
            "pageNo": pageNo,
            "basDt": basDt,
            "itmsNm": itmsNm,
        }
        params.update(kwargs)

        data = await self._request(
            "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getGetDerivativesPriceInfo",
            params={k: v for k, v in params.items() if v is not None},
        )
        return DataPortalResponse[DerivativesPriceInfoItem].model_validate(data)
