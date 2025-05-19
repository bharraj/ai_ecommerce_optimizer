from pydantic import BaseModel, Field

class ItemRequest(BaseModel):
    product: str = Field(..., description='Item name')
    color: str = Field(..., description='Chosen color')

class N8nResponse(BaseModel):
    status: str
    detail: str | dict | None