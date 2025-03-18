from typing import List, Optional, Dict
from pydantic import BaseModel
from enum import StrEnum

class HTTP_METHODS(StrEnum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    CONNECT = 'CONNECT'
    TRACE = 'TRACE'

class TASK_STATUS(StrEnum):
    READY = 'ready'
    RUNNING = 'running'
    PAUSE = 'pause'
    WAIT = 'wait'
    ERROR = 'error'
    DONE = 'done'

class Request_Extra_Opt(BaseModel):
    methed: Optional[HTTP_METHODS] = None
    header: Optional[Dict[str, str]] = None
    body: Optional[str] = None
    trackers: Optional[List[str]] = None

class ResolveRequest_Response_Res_File(BaseModel):
    name: str
    path: str
    size: int
    ctime: str | None # ISO8601 UTC 
    # req: None

class ResolveRequest_Response_Res(BaseModel):
    name: str
    size: int
    range: bool
    files: List[ResolveRequest_Response_Res_File]
    hash: str

class ResolveRequest_ResponseData(BaseModel):
    id: str
    res: ResolveRequest_Response_Res

class CreateTask_DownloadOpt_Extra(BaseModel):
    autoTorrent: Optional[bool] = None
    connections: int

class CreateTask_DownloadOpt(BaseModel):
    name: Optional[str] = None
    path: Optional[str] = None
    selectFiles: List[int] | None = None
    extra: CreateTask_DownloadOpt_Extra = CreateTask_DownloadOpt_Extra(connections=16)
  