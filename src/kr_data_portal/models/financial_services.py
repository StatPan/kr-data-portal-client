from pydantic import BaseModel


class StockPriceInfoItem(BaseModel):
    """Model for getStockPriceInfo item."""

    # Note: In production, these fields should be mapped based on actual API response
    # For now, we use dynamic fields or common ones if known.
    # We'll define some common stock fields here.
    basDt: str | None = None
    srtnCd: str | None = None
    isinCd: str | None = None
    itmsNm: str | None = None
    mrktCtg: str | None = None
    clpr: str | None = None
    vs: str | None = None
    fltRt: str | None = None
    mkp: str | None = None
    hipr: str | None = None
    lopr: str | None = None
    trqu: str | None = None
    trPrc: str | None = None
    lstgStCnt: str | None = None
    mrktTotAmt: str | None = None


class EtfPriceInfoItem(BaseModel):
    """Model for getEtfPriceInfo item."""

    # Note: In production, these fields should be mapped based on actual API response
    # For now, we use dynamic fields or common ones if known.
    # We'll define some common stock fields here.
    basDt: str | None = None
    srtnCd: str | None = None
    isinCd: str | None = None
    itmsNm: str | None = None
    mrktCtg: str | None = None
    clpr: str | None = None
    vs: str | None = None
    fltRt: str | None = None
    mkp: str | None = None
    hipr: str | None = None
    lopr: str | None = None
    trqu: str | None = None
    trPrc: str | None = None
    lstgStCnt: str | None = None
    mrktTotAmt: str | None = None


class EtnPriceInfoItem(BaseModel):
    """Model for getEtnPriceInfo item."""

    # Note: In production, these fields should be mapped based on actual API response
    # For now, we use dynamic fields or common ones if known.
    # We'll define some common stock fields here.
    basDt: str | None = None
    srtnCd: str | None = None
    isinCd: str | None = None
    itmsNm: str | None = None
    mrktCtg: str | None = None
    clpr: str | None = None
    vs: str | None = None
    fltRt: str | None = None
    mkp: str | None = None
    hipr: str | None = None
    lopr: str | None = None
    trqu: str | None = None
    trPrc: str | None = None
    lstgStCnt: str | None = None
    mrktTotAmt: str | None = None


class DerivativesPriceInfoItem(BaseModel):
    """Model for getDerivativesPriceInfo item."""

    # Note: In production, these fields should be mapped based on actual API response
    # For now, we use dynamic fields or common ones if known.
    # We'll define some common stock fields here.
    basDt: str | None = None
    srtnCd: str | None = None
    isinCd: str | None = None
    itmsNm: str | None = None
    mrktCtg: str | None = None
    clpr: str | None = None
    vs: str | None = None
    fltRt: str | None = None
    mkp: str | None = None
    hipr: str | None = None
    lopr: str | None = None
    trqu: str | None = None
    trPrc: str | None = None
    lstgStCnt: str | None = None
    mrktTotAmt: str | None = None
