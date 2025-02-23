from pydantic import BaseModel

class ContinueATask_Response(BaseModel):
    code: int
    msg: str
    data: None
