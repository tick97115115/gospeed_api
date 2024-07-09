from pydantic import BaseModel

class GetServerInfoResponse_Data(BaseModel):
    version: str
    runtime: str
    os: str
    arch: str
    inDocker: bool

class GetServerInfo_Response(BaseModel):
    code: int
    msg: str
    data: GetServerInfoResponse_Data
