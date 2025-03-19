from pydantic import BaseModel
from .get_task_list import Task

class GetTaskInfo_Response(BaseModel):
    code: int
    msg: str
    data: Task
    @property
    def task_info(self):
        return self.data

