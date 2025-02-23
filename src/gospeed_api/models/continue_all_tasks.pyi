from pydantic import BaseModel

class ContinueAllTasks_Response(BaseModel):
    code: int
    msg: str
    data: None
