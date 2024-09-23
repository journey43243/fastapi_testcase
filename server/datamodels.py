from pydantic import BaseModel


class ProductValidation(BaseModel):
    name: str
    product_type_id: int
