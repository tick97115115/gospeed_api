from . import CreateTask_DownloadOpt as CreateTask_DownloadOpt
from pydantic import BaseModel

class TaskUrl(BaseModel):
    url: str

class CreateABatchOfTasks(BaseModel):
    reqs: list[TaskUrl]
    opt: CreateTask_DownloadOpt

class CreateABatchOfTasks_Response(BaseModel):
    code: int
    msg: str
    data: list[str]
