from typing import List, Optional, Dict
from pydantic import BaseModel
from enum import Enum

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

  def __str__(self) -> str:
    return self.value
  def  __repr__(self) -> str:
    return self.value

class TASK_STATUS(Enum):
  READY = 'ready'
  RUNNING = 'running'
  PAUSE = 'pause'
  WAIT = 'wait'
  ERROR = 'error'
  DONE = 'done'

  def __str__(self) -> str:
    return self.value
  def  __repr__(self) -> str:
    return self.value
  
class Request_Extra_Opt(BaseModel):
  methed: Optional[HTTP_METHODS] = None
  header: Optional[Dict[str, str]] = None
  body: Optional[str] = None
  trackers: Optional[List[str]] = None

class ResolveRequest_Response_Res_File_Req(BaseModel):
  url: str
  extra: Optional[Request_Extra_Opt] = None
  labels: Optional[Dict[str, str]] = None

class ResolveRequest_Response_Res_File(BaseModel):
  name: str
  path: str
  size: int
  #ctime: Optional[str] # ISO8601 UTC 

class ResolveRequest_Response_Res(BaseModel):
  name: str
  size: int
  range: bool
  files: List[ResolveRequest_Response_Res_File]
  hash: Optional[str] = None

class ResolveRequest_ResponseData(BaseModel):
  id: str
  res: ResolveRequest_Response_Res

class CreateTask_DownloadOpt_Extra(BaseModel):
  autoTorrent: bool
  connections: int

class CreateTask_DownloadOpt(BaseModel):
  name: str
  path: str
  selectFiles: List[int]
  extra: CreateTask_DownloadOpt_Extra
  