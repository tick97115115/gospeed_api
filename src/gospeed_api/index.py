from urllib.parse import urljoin
from typing import Set, Dict

import requests
import httpx
import anyio

from gospeed_api.models.delete_tasks import DeleteTasks_Response

from .models.get_server_info import GetServerInfo_Response
from .models.resolve_a_request import ResolveRequest, ResolveRequest_Response
from .models.get_task_list import GetTaskList_Response
from .models.create_a_task import CreateATask_fromResolvedId, CreateATask_Response, CreateATask_fromUrl
from .models.delete_a_task import DeleteATask_Response
from .models.create_a_batch_of_tasks import CreateABatchOfTasks, CreateABatchOfTasks_Response
from .models.get_task_info import GetTaskInfo_Response
from .models.pause_a_task import PauseATask_Response
from .models.continue_a_task import ContinueATask_Response
from .models.pause_all_tasks import PauseAllTasks_Response
from .models.continue_all_tasks import ContinueAllTasks_Response
from .models import TASK_STATUS

def my_url_join(first: str, last: str) -> str:
    """Checking slash symbol between url and path string."""
    if (first[-1] != '/' and last[0] != '/'):
        first = first + '/'
    return str(urljoin(first, last))

def check_response_and_return_data(res: httpx.Response) -> Dict:
    """check response status code then return json data"""
    if (res.status_code == 200):
        return res.json()
    res.raise_for_status()
    return None

TIMEOUT_SECONDS: int = 8

def construct_status_query_params(status: Set[TASK_STATUS] | None) -> Dict:
    """check status set if is null"""
    if (isinstance(status, Set) and len(status) == 0):
        raise TypeError('status Set should not be empty!')
    if (status is not None):
        return {'status': list(status)}
    return {}

class GospeedClient:
    """This class represent Gospeed Rest API interface, initializing with Gospeed API address."""

    def __init__(self, url) -> None:
        # prevent string conjunction bug while using urllib.parse.urljoin()
        if (url[-1] != '/'):
            url = url + '/'
        self.url = url
        self.endpoint_info = urljoin(self.url, 'api/v1/info')
        self.endpoint_resolve = urljoin(self.url, 'api/v1/resolve')
        self.endpoint_task = urljoin(self.url, 'api/v1/tasks')
        self.endpoint_task_batch = urljoin(self.url, 'api/v1/tasks/batch')
        self.endpoint_tasks_pause = urljoin(self.url, 'api/v1/tasks/pause')
        self.endpoint_tasks_continue = urljoin(self.url, 'api/v1/tasks/continue')

    def get_server_info(self) -> GetServerInfo_Response:
        """Return Gospeed server info"""
        res = requests.get(url=self.endpoint_info, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return GetServerInfo_Response(**json)
        
    def resolve_a_request(self, param: ResolveRequest) -> ResolveRequest_Response:
        """resolve request link and return ResolveRequest_Response data model object."""
        res = requests.post(url=self.endpoint_resolve, data=param.model_dump_json(), headers={"content-type": "application/json", "accept": "application/json"}, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return ResolveRequest_Response(**json)

    def get_task_list(self, status: Set[TASK_STATUS] = None) -> GetTaskList_Response:
        """Get all tasks according to specified status."""
        query_paramter=construct_status_query_params(status=status)

        res = requests.get(url=self.endpoint_task, params=query_paramter, headers={'accept': 'application/json'}, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return GetTaskList_Response(**json)

    def create_a_task_from_resolved_id(self, param: CreateATask_fromResolvedId) -> CreateATask_Response:
        r"""receive CreateATask_fromResolvedId object as paramter. see src\gospeed_api\models\create_a_task.py for detail return data structure."""
        res = requests.post(url=self.endpoint_task, headers={"accept": "application/json", "content-type": "application/json"}, data=param.model_dump_json(), timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return CreateATask_Response(**json)

    def create_a_task_from_url(self, param: CreateATask_fromUrl) -> CreateATask_Response:
        """Directly create a task instead of resolve it's information first."""
        res = requests.post(self.endpoint_task, headers={"accept": "application/json", "content-type": "application/json"}, data=param.model_dump_json(), timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return CreateATask_Response(**json)

    def delete_a_task(self, rid: str, force: bool = False) -> DeleteATask_Response:
        """Delete a task by specify it's id, force if true will delete the file also."""
        res = requests.delete(url=my_url_join(self.endpoint_task, rid), params={'force': str(force).lower()}, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return DeleteATask_Response(**json)

    def create_a_batch_of_tasks(self, data: CreateABatchOfTasks) -> CreateABatchOfTasks_Response:
        """Create multiple tasks at once."""
        res = requests.post(self.endpoint_task_batch, headers={"accept": "application/json", "content-type": "application/json"}, data=data.model_dump_json(), timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return CreateABatchOfTasks_Response(**json)

    def delete_tasks(self, status: Set[TASK_STATUS] = None, force: bool = False) -> DeleteTasks_Response:
        """Delete tasks according to specified status."""
        query_paramter = construct_status_query_params(status)
        query_paramter['force'] = str(force).lower()
        
        res = requests.delete(self.endpoint_task, params=query_paramter, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return DeleteTasks_Response(**json)

    def get_task_info(self, rid: str) -> GetTaskInfo_Response:
        """Get a task info from it's id."""
        res = requests.get(url=my_url_join(self.endpoint_task, rid), headers={"accept": "application/json"}, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return GetTaskInfo_Response(**json)

    def pause_a_task(self, rid: str) -> PauseATask_Response:
        """Pause a task download according to task id."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'pause')
        res = requests.put(url=url, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return PauseATask_Response(**json)

    def continue_a_task(self, rid: str) -> ContinueATask_Response:
        """Continue a stop task according to task id."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'continue')
        res = requests.put(url=url, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return ContinueATask_Response(**json)

    def pause_all_tasks(self) -> PauseAllTasks_Response:
        """Palse every tasks inside Gospeed downloader."""
        res = requests.put(url=self.endpoint_tasks_pause, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return PauseAllTasks_Response(**json)

    def continue_all_tasks(self) -> ContinueAllTasks_Response:
        """Continue every tasks inside Gospeed downloader."""
        res = requests.put(url=self.endpoint_tasks_continue, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return ContinueAllTasks_Response(**json)

class AsyncGospeedClient(GospeedClient):
    """Async implementation"""
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.httpx_client = httpx.AsyncClient()

    def __del__(self):
        # self.httpx_client.close()
        pass

    async def async_get_server_info(self) -> GetServerInfo_Response:
        """Async implementation of get_server_info function."""
        res = await self.httpx_client.get(self.endpoint_info, timeout=TIMEOUT_SECONDS)
        res = requests.get(url=self.endpoint_info, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return GetServerInfo_Response(**json)
        
    async def async_resolve_a_request(self, param: ResolveRequest) -> ResolveRequest_Response:
        """Async implementation of resolve_a_request."""
        res = await self.httpx_client.post(url=self.endpoint_resolve, content=param.model_dump_json(), headers={"content-type": "application/json", "accept": "application/json"}, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return ResolveRequest_Response(**json)
    
    async def async_get_task_list(self, status: Set[TASK_STATUS] = None) -> GetTaskList_Response:
        """Async implementation of get_task_list."""
        query_paramter = construct_status_query_params(status)
        res = await self.httpx_client.get(url=self.endpoint_task, params=query_paramter,headers={'accept': 'application/json'}, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return GetTaskList_Response(**json)
    
    async def async_create_a_task_from_resolved_id(self, param:CreateATask_fromResolvedId) -> CreateATask_Response:
        """Async implementation of create_a_task_from_resolved_id."""
        res = await self.httpx_client.post(url=self.endpoint_task, headers={"accept": "application/json", "content-type": "application/json"}, content=param.model_dump_json(), timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return CreateATask_Response(**json)
    
    async def async_create_a_task_from_url(self, param: CreateATask_fromUrl) -> CreateATask_Response:
        """Async implementation of create_a_task_from_url."""
        res = await self.httpx_client.post(self.endpoint_task, headers={"accept": "application/json", "content-type": "application/json"}, content=param.model_dump_json(), timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return CreateATask_Response(**json)
    
    async def async_delete_a_task(self, rid: str, force: bool = False) -> DeleteATask_Response:
        """Async implementation of delete_a_task."""
        res = await self.httpx_client.delete(url=my_url_join(self.endpoint_task, rid), params=str(force).lower(), timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return DeleteATask_Response(**json)
    
    async def async_create_a_batch_of_tasks(self, data: CreateABatchOfTasks) -> CreateABatchOfTasks_Response:
        """Async implementation of create_a_batch_of_tasks."""
        res = await self.httpx_client.post(self.endpoint_task_batch, headers={"accept": "application/json", "content-type": "application/json"}, content=data.model_dump_json(), timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return CreateABatchOfTasks_Response(**json)
    
    async def async_delete_tasks(self, status: Set[TASK_STATUS] = None, force: bool = False) -> DeleteTasks_Response:
        """Async implementation of delete_tasks."""
        query_paramter = construct_status_query_params(status)
        query_paramter['force'] = str(force).lower()
        res = await self.httpx_client.delete(url=self.endpoint_task, params=query_paramter, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return DeleteTasks_Response(**json)
    
    async def async_get_task_info(self, rid: str) -> GetTaskInfo_Response:
        """Async implementation of get_task_info."""
        res = await self.httpx_client.get(url=my_url_join(self.endpoint_task, rid), headers={"accept": "application/json"}, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return GetTaskInfo_Response(**json)
    
    async def async_pause_a_task(self, rid: str) -> PauseATask_Response:
        """Async implementation of pause_a_task."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'pause')
        res = await self.httpx_client.put(url, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return PauseATask_Response(**json)
    
    async def async_continue_a_task(self, rid: str) -> ContinueATask_Response:
        """Async implementation of continue_a_task."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'continue')
        res = await self.httpx_client.put(url, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return ContinueATask_Response(**json)
    
    async def async_pause_all_tasks(self) -> PauseAllTasks_Response:
        """Async implementation of pause_all_tasks."""
        res = await self.httpx_client.put(self.endpoint_tasks_pause, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return PauseAllTasks_Response(**json)
    
    async def async_continue_all_tasks(self) -> PauseAllTasks_Response:
        """Async implementation of continue_all_tasks."""
        res = await self.httpx_client.put(url=self.endpoint_tasks_continue, timeout=TIMEOUT_SECONDS)
        json = check_response_and_return_data(res)
        return ContinueAllTasks_Response(**json)
