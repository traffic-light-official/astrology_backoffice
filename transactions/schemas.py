from datetime import datetime


from pydantic import BaseModel, field_validator, Field, AliasPath


class TransactionInfo(BaseModel):
    id: str
    client_reference_id: str | int
    created: int
    currency: str
    payment_status: str
    amount_total: int
    email: str = Field(default=None, validation_alias=AliasPath('customer_details', 'email'))
    country: str = Field(default=None, validation_alias=AliasPath('customer_details', 'address', 'country'))
    quantity: int = Field(validation_alias=AliasPath('line_items', 'data', 0, 'quantity'))
    presentment_amount: int = Field(default=None, validation_alias=AliasPath('presentment_details',
                                                                             'presentment_amount'))
    presentment_currency: str = Field(default=None, validation_alias=AliasPath('presentment_details',
                                                                               'presentment_currency'))


    @field_validator("created")
    @classmethod
    def created_datetime(cls, v: int):
        return datetime.fromtimestamp(v)


    @field_validator("client_reference_id")
    @classmethod
    def type_client_reference(cls, v: str):
        return int(v)

    @field_validator("presentment_amount")
    @classmethod
    def validate_presentment_amount(cls, v: int):
        if v is not None:
            v = v * 0.01
            return v
        return v

    @field_validator("amount_total")
    @classmethod
    def validate_total_amount(cls, v: int):
        v = v * 0.01
        return v
