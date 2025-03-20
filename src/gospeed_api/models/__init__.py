from typing import List, Optional, Dict
from pydantic import BaseModel
from enum import StrEnum

class GopeedAPIError(Exception):
    def __init__(self, code: int, msg: str, summary: str):
        super().__init__(summary)
        self.code = code
        self.msg = msg

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
    """
    method, header, body field only for HTTP task, trackers only for BT task.

    If a task is BT download task, then extra only contain 'trackers' field.
    Else for a HTTP download task, it will contain method, header, body fields.

    We could detect a task if ts is a BT or HTTP download task by check 'trackers' field's existence.
    """
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
    extra: CreateTask_DownloadOpt_Extra | None = None

class GopeedResponse(BaseModel):
    code: int
    msg: str
    @property
    def is_success(self) -> bool:
        if self.code == 0:
            return True
        return False
    
    @property
    def summary(self) -> str:
        return f"\nGopeed response code: \"{self.code}\", \n{self.msg}"
    
    def raise_error(self):
        raise GopeedAPIError(code=self.code, msg=self.msg, summary=self.summary)
