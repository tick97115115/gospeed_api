from pydantic import BaseModel

class DeleteATask_Response(BaseModel):
    code: int
    msg: str
    data: None