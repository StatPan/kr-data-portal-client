from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class ResponseHeader(BaseModel):
    resultCode: str
    resultMsg: str

class ResponseBody(BaseModel, Generic[T]):
    numOfRows: int
    pageNo: int
    totalCount: int
    items: dict  # Contains "item": List[T]

class ApiResponse(BaseModel, Generic[T]):
    header: ResponseHeader
    body: ResponseBody[T]

class StockPriceItem(BaseModel):
    basDt: str = Field(..., description="기준일자")
    srtnCd: str = Field(..., description="단축코드")
    isinCd: str = Field(..., description="ISIN코드")
    itmsNm: str = Field(..., description="종목명")
    mrktCtg: str = Field(..., description="시장구분")
    clpr: str = Field(..., description="종가")
    vs: str = Field(..., description="대비")
    fltRt: str = Field(..., description="등락률")
    mkp: str = Field(..., description="시가")
    hipr: str = Field(..., description="고가")
    lopr: str = Field(..., description="저가")
    trqu: str = Field(..., description="거래량")
    trPrc: str = Field(..., description="거래대금")
    lstgStcn: str = Field(..., description="상장주식수")
    mrktTotAmt: str = Field(..., description="시가총액")

class BaseApiResponse(BaseModel, Generic[T]):
    response: ApiResponse[T]
