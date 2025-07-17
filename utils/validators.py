from pydantic import BaseModel
from typing import Literal

class RequestModel(BaseModel):
    type: Literal["request", "pre_request"]
    name: str
    rank: str
    branch: str
    code: str
    
class RequestActionModel(BaseModel):
    type: Literal['accepted', 'denied']
    code: str
    