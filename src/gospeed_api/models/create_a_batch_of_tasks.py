from pydantic import BaseModel
from typing import List
from . import CreateTask_DownloadOpt

class TaskUrl(BaseModel):
    url: str

class CreateABatchOfTasks(BaseModel):
    reqs: List[TaskUrl]
    opt: CreateTask_DownloadOpt

class CreateABatchOfTasks_Response(BaseModel):
    code: int
    msg: str
    data: List[str]