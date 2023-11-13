from pydantic import BaseModel


class Order(BaseModel):
    selected: str
    method: str
    contact: str
