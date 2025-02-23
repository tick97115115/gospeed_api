from . import Request_Extra_Opt as Request_Extra_Opt, ResolveRequest_ResponseData as ResolveRequest_ResponseData
from pydantic import BaseModel

class ResolveRequest(BaseModel):
    url: str
    extra: Request_Extra_Opt | None
    lables: dict[str, str] | None

class ResolveRequest_Response(BaseModel):
    code: int
    msg: str
    data: ResolveRequest_ResponseData | None
