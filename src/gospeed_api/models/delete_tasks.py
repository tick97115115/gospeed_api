from pydantic import BaseModel

class DeleteTasks_Response(BaseModel):
    code: int
    msg: str
    data: None