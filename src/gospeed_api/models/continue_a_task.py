from pydantic import BaseModel

class ContinueATask_Response(BaseModel):
    """The returned object of method \"continue_a_task\"."""
    code: int
    msg: str
    data: None