from pydantic import BaseModel, StrictInt, StrictFloat

class GetTaskStats_Response_Stats(BaseModel):
    totalPeers: StrictInt
    activePeers: StrictInt
    connectedSeeders: StrictInt
    seedBytes: StrictInt
    seedRatio: StrictFloat
    seedTime: StrictInt

class GetTaskStats_Response(BaseModel):
    code: StrictInt
    msg: str
    data: GetTaskStats_Response_Stats