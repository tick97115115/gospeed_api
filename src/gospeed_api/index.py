from .models.get_server_info import GetServerInfo_Response
from .models.post_resolve_a_request import ResolveRequest, ResolveRequest_Response, ResolveRequest_ResponseData
from .models.get_task_list import GetTaskList_Response
import requests
from requests import Response
from urllib.parse import urljoin
from pydantic import BaseModel
from typing import Set
from .models import TASK_STATUS

def convert_response_json_to_object(res: Response, pydantic_model: BaseModel):
  pass

class GospeedClient:
  def __init__(self, url) -> None:
    # prevent string conjunction bug while using urllib.parse.urljoin()
    if (url[-1] != '/'):
      url = url + '/'
    self.url = url
    self.endpoint_get_server_info = urljoin(self.url, 'api/v1/info')
    self.endpoint_resolve_a_request = urljoin(self.url, 'api/v1/resolve')
    self.endpoint_get_task_list = urljoin(self.url, 'api/v1/tasks')
  
  def get_server_info(self) -> GetServerInfo_Response:
    res = requests.get(url=self.endpoint_get_server_info)
    if res.status_code == 200:
      json = res.json()
      return GetServerInfo_Response(**json)
    else:
      res.raise_for_status()
  
  def resolve_a_request(self, data: ResolveRequest) -> ResolveRequest_Response:
    res = requests.post(url=self.endpoint_resolve_a_request, data=data.model_dump_json(), headers={"content-type": "application/json", "accept": "application/json"})
    if res.status_code == 200:
      json = res.json()
      return ResolveRequest_Response(**json)
    else:
      res.raise_for_status()

  def get_task_list(self, status: Set[TASK_STATUS]) -> GetTaskList_Response:
    res = requests.get(url=self.endpoint_get_task_list, params={'status': list(status)}, headers={'accept': 'application/json'})
    if res.status_code == 200:
      json = res.json()
      return GetTaskList_Response(**json)
    else:
      res.raise_for_status()
