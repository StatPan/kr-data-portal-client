
import pytest
from pydantic import BaseModel
from kr_data_portal.models.base import DataPortalResponse, BaseResponse, ResponseHeader, ResponseBody

class MockItem(BaseModel):
    name: str
    value: int

def test_items_parsing_with_dict_body():
    # 시크릿이나 복잡한 구조로 인해 body가 dict로 들어온 경우를 시뮬레이션
    raw_response = {
        "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."},
            "body": {
                "items": {
                    "item": [
                        {"name": "Samsung", "value": 55400},
                        {"name": "SK Hynix", "value": 180000}
                    ]
                },
                "numOfRows": 10,
                "pageNo": 1,
                "totalCount": 2
            }
        }
    }
    
    # DataPortalResponse 생성
    response = DataPortalResponse[MockItem].model_validate(raw_response)
    
    # items() 호출 및 검증
    items = response.items(MockItem)
    
    assert len(items) == 2
    assert isinstance(items[0], MockItem)
    assert items[0].name == "Samsung"
    assert items[0].value == 55400

def test_items_parsing_with_single_item_dict():
    # 아이템이 하나일 때 dict로 들어오는 경우 시뮬레이션
    raw_response = {
        "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."},
            "body": {
                "items": {
                    "item": {"name": "LG Energy", "value": 400000}
                }
            }
        }
    }
    
    response = DataPortalResponse[MockItem].model_validate(raw_response)
    items = response.items(MockItem)
    
    assert len(items) == 1
    assert items[0].name == "LG Energy"
