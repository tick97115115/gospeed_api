from typing import Optional, Dict
from . import Request_Extra_Opt, ResolveRequest_ResponseData, GopeedResponse
from pydantic import BaseModel

class ResolveRequest(BaseModel):
    url: str
    extra: Optional[Request_Extra_Opt] = None
    labels: Optional[Dict[str, str]] = None

class ResolveRequest_Response(GopeedResponse):
    data: Optional[ResolveRequest_ResponseData] = None
