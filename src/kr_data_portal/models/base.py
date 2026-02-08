from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ResponseHeader(BaseModel):
    resultCode: str
    resultMsg: str


class ResponseBody(BaseModel, Generic[T]):
    items: Any = None
    numOfRows: int = 0
    pageNo: int = 0
    totalCount: int = 0


class BaseResponse(BaseModel, Generic[T]):
    header: ResponseHeader
    body: ResponseBody[T] | Any | None = None


class DataPortalResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    response: BaseResponse[T]

    def items(self, model_cls: type[T]) -> list[T]:
        body = self.response.body
        if not body:
            return []

        # 1. Extract items_field flexibly from Model or Dict
        items_field = None
        if isinstance(body, ResponseBody):
            items_field = body.items
        elif isinstance(body, dict):
            items_field = body.get("items")
        else:
            # Fallback for cases where it might be a different object type
            items_field = getattr(body, "items", None)

        if not items_field:
            return []

        # 2. Handle the "item" wrapper (common in Data Portal APIs)
        raw_list = []
        if isinstance(items_field, dict):
            item = items_field.get("item")
            if isinstance(item, list):
                raw_list = item
            elif item is not None:
                raw_list = [item]
        elif isinstance(items_field, list):
            raw_list = items_field
        
        # 3. Final validation and conversion
        result = []
        for i in raw_list:
            if isinstance(i, dict):
                try:
                    result.append(model_cls.model_validate(i))
                except Exception:
                    # If validation fails, keep as dict or skip? 
                    # Prefer keeping raw dict if validation fails to avoid data loss
                    result.append(i)
            else:
                result.append(i)
        
        return result
