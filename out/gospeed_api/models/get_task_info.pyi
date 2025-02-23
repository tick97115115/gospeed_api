from .get_task_list import Task as Task
from pydantic import BaseModel

class GetTaskInfo_Response(BaseModel):
    code: int
    msg: str
    data: Task
