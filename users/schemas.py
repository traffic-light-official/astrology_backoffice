from datetime import datetime


from pydantic import BaseModel, field_validator


class PresentmentDetails(BaseModel):
    presentment_amount: int
    presentment_currency: str


class Data(BaseModel):
    quantity: int


class LineItems(BaseModel):
    data: list[Data]


class TransactionInfo(BaseModel):
    client_reference_id: str
    created: int
    currency: str
    payment_status: str
    amount_total: int
    line_items: LineItems
    presentment_details: PresentmentDetails | None = None

    @field_validator("created")
    @classmethod
    def created_datetime(cls, v: int):
        return datetime.fromtimestamp(v)

    @field_validator("client_reference_id")
    @classmethod
    def type_client_reference(cls, v: str):
        return int(v)
