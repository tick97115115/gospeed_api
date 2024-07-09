from pydantic import BaseModel

class ContinueAllTasks_Response(BaseModel):
    """The return object of method\"continue_all_tasks\"."""
    code: int
    msg: str
    data: None