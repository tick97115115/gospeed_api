from enum import Enum
from pydantic import BaseModel

class HTTP_METHODS(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    CONNECT = 'CONNECT'
    TRACE = 'TRACE'

class TASK_STATUS(Enum):
    READY = 'ready'
    RUNNING = 'running'
    PAUSE = 'pause'
    WAIT = 'wait'
    ERROR = 'error'
    DONE = 'done'

class Request_Extra_Opt(BaseModel):
    methed: HTTP_METHODS | None
    header: dict[str, str] | None
    body: str | None
    trackers: list[str] | None

class ResolveRequest_Response_Res_File_Req(BaseModel):
    url: str
    extra: Request_Extra_Opt | None
    labels: dict[str, str] | None

class ResolveRequest_Response_Res_File(BaseModel):
    name: str
    path: str
    size: int
    ctime: str | None

class ResolveRequest_Response_Res(BaseModel):
    name: str
    size: int
    range: bool
    files: list[ResolveRequest_Response_Res_File]
    hash: str

class ResolveRequest_ResponseData(BaseModel):
    id: str
    res: ResolveRequest_Response_Res

class CreateTask_DownloadOpt_Extra(BaseModel):
    autoTorrent: bool | None
    connections: int

class CreateTask_DownloadOpt(BaseModel):
    name: str | None
    path: str | None
    selectFiles: list[int]
    extra: CreateTask_DownloadOpt_Extra
