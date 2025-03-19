from .resolve_a_request import ResolveRequest
from pydantic import BaseModel
from . import CreateTask_DownloadOpt

class CreateATask_fromResolvedId(BaseModel):
    rid: str
    opt: CreateTask_DownloadOpt | None = None

class CreateATask_FromUrl(BaseModel):
    req: ResolveRequest
    opt: CreateTask_DownloadOpt | None = None

class CreateATask_Response(BaseModel):
    code: int
    msg: str
    data: str # this is created task id
    @property
    def task_id(self):
        return self.data