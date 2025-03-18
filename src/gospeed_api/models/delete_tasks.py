from pydantic import BaseModel
from . import TASK_STATUS

class DeleteTasks_Response(BaseModel):
    code: int
    msg: str
    data: None

class DeleteTasks_Request(BaseModel):
    id: list[str] | None = None
    status: list[TASK_STATUS] | None = None
    notStatus: list[TASK_STATUS] | None = None
    force: bool = False