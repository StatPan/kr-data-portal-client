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
        if not self.response.body:
            return []

        items_field = None
        if isinstance(self.response.body, ResponseBody):
            items_field = self.response.body.items
        elif isinstance(self.response.body, dict):
            items_field = self.response.body.get("items")

        if not items_field:
            return []

        raw_list = []
        if isinstance(items_field, dict):
            item = items_field.get("item")
            if isinstance(item, list):
                raw_list = item
            elif item:
                raw_list = [item]
        elif isinstance(items_field, list):
            raw_list = items_field

        return [model_cls.model_validate(i) if isinstance(i, dict) else i for i in raw_list]
