from . import CreateTask_DownloadOpt, ResolveRequest_Response_Res_File_Req
from pydantic import BaseModel

class CreateATask_fromResolvedId(BaseModel):
    rid: str
    opt: CreateTask_DownloadOpt

class CreateATask_fromUrl(BaseModel):
    req: ResolveRequest_Response_Res_File_Req
    opt: CreateTask_DownloadOpt

class CreateATask_Response(BaseModel):
    code: int
    msg: str
    data: str # this is created task id