from pydantic import BaseModel

class PauseAllTasks_Response(BaseModel):
    code: int
    msg: str
    data: None