from pydantic import BaseModel
from .get_task_list import Task

class GetTaskInfo_Response(BaseModel):
    code: int
    msg: str
    data: Task

