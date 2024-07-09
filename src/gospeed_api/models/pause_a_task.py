from pydantic import BaseModel

class PauseATask_Response(BaseModel):
    code: int
    msg: str
    data: None