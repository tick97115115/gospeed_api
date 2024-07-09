from pydantic import BaseModel
from typing import List, Optional
from . import CreateTask_DownloadOpt, ResolveRequest_Response_Res, ResolveRequest_Response_Res_File_Req, TASK_STATUS

class Task_Progress(BaseModel):
    used: int
    speed: int
    downloaded: int

class Task_Meta(BaseModel):
    opts: CreateTask_DownloadOpt
    res: Optional[ResolveRequest_Response_Res]
    req: ResolveRequest_Response_Res_File_Req

class Task(BaseModel):
    id: str
    meta: Task_Meta
    status: TASK_STATUS
    protocol: str
    progress: Task_Progress
    createdAt: str
    updatedAt: str

class GetTaskList_Response(BaseModel):
    code: int
    msg: str
    data: List[Task]