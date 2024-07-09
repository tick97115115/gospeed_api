from typing import Optional, Dict
from . import Request_Extra_Opt, ResolveRequest_ResponseData
from pydantic import BaseModel

class ResolveRequest(BaseModel):
    url: str
    extra: Optional[Request_Extra_Opt] = None
    lables: Optional[Dict[str, str]] = None

class ResolveRequest_Response(BaseModel):
    code: int
    msg: str
    data: Optional[ResolveRequest_ResponseData] = None