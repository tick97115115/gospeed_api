from urllib.parse import urljoin
from typing import List, Dict
from httpx import AsyncClient, Client, Response

from .models.get_server_info import GetServerInfo_Response
from .models.resolve_a_request import ResolveRequest, ResolveRequest_Response
from .models.get_task_list import GetTaskList_Response
from .models.create_a_task import CreateATask_fromResolvedId, CreateATask_Response, CreateATask_FromUrl
from .models.delete_a_task import DeleteATask_Response
from .models.create_a_batch_of_tasks import CreateABatchOfTasks, CreateABatchOfTasks_Response, TaskUrl
from .models.get_task_info import GetTaskInfo_Response
from .models.pause_a_task import PauseATask_Response
from .models.continue_a_task import ContinueATask_Response
from .models.pause_all_tasks import PauseAllTasks_Response
from .models.continue_all_tasks import ContinueAllTasks_Response
from .models.delete_tasks import DeleteTasks_Request, DeleteTasks_Response
from .models.get_task_stats import GetTaskStats_Response
from .models import TASK_STATUS, CreateTask_DownloadOpt, Request_Extra_Opt

def obj_filter(obj: Dict) -> Dict | None:
    col = {}
    for k, v in obj.items():
        if v == None:
            continue
        elif isinstance(v, List) and len(v) == 0:
            continue
        else:
            col[k] = v

    if len(col.keys()) == 0:
        return None
    else:
        return col


def my_url_join(first: str, last: str) -> str:
    """Checking slash symbol between url and path string."""
    if (first[-1] != '/' and last[0] != '/'):
        first = first + '/'
    return str(urljoin(first, last))

def check_response_and_return_data(res: Response) -> Dict:
    """check response status code then return json data"""
    if (300 <= res.status_code or res.status_code <= 199):
        res.raise_for_status()
    return res.json()

class GospeedAPI:
    def __init__(self, gopeed_host: str, httpx_client: Client = Client(), async_httpx_client: AsyncClient = AsyncClient()):
        self.httpx_client = httpx_client
        self.async_httpx_client = async_httpx_client
        # prevent string conjunction bug while using urllib.parse.urljoin()
        if (gopeed_host[-1] != '/'):
            url = gopeed_host + '/'
        self.url = gopeed_host
        self.endpoint_info = urljoin(self.url, 'api/v1/info')
        self.endpoint_resolve = urljoin(self.url, 'api/v1/resolve')
        self.endpoint_task = urljoin(self.url, 'api/v1/tasks')
        self.endpoint_task_batch = urljoin(self.url, 'api/v1/tasks/batch')
        self.endpoint_tasks_pause = urljoin(self.url, 'api/v1/tasks/pause')
        self.endpoint_tasks_continue = urljoin(self.url, 'api/v1/tasks/continue')

    def get_server_info(self) -> GetServerInfo_Response:
        """Return Gospeed server info"""
        res = self.httpx_client.get(url=self.endpoint_info)
        json = check_response_and_return_data(res)
        return GetServerInfo_Response(**json)
    
    async def async_get_server_info(self) -> GetServerInfo_Response:
        """Async implementation of get_server_info function."""
        res = await self.async_httpx_client.get(self.endpoint_info)
        json = check_response_and_return_data(res)
        return GetServerInfo_Response(**json)
    
    def resolve_a_request(self, url: str, extra: Request_Extra_Opt | None = None, labels: Dict[str, str] | None = None) -> ResolveRequest_Response:
        """resolve request link and return ResolveRequest_Response data model object."""
        param = ResolveRequest(url=url, extra=extra, labels=labels)
        res = self.httpx_client.post(url=self.endpoint_resolve, json=param.model_dump())
        json = check_response_and_return_data(res)
        return ResolveRequest_Response(**json)
    
    async def async_resolve_a_request(self, url: str, extra: Request_Extra_Opt | None = None, labels: Dict[str, str] | None = None) -> ResolveRequest_Response:
        """Async implementation of resolve_a_request."""
        param = ResolveRequest(url=url, extra=extra, labels=labels)
        res = await self.async_httpx_client.post(url=self.endpoint_resolve, json=param.model_dump())
        json = check_response_and_return_data(res)
        return ResolveRequest_Response(**json)

    def get_task_list(self,id_list: List[str], status: List[TASK_STATUS] | None = None, notStatus: List[TASK_STATUS] | None = None) -> GetTaskList_Response:
        """Get all tasks according to specified status."""
        # Shouldn't 
        # URL('http://127.0.0.1:9999/api/v1/tasks?id=_bzk6rchQMj78qJjmMAqq&id=KFSx1z3wXV7nCT7p43OcT&id=P6mNHl6XBlCfb9GBYyZAl&id=H21G0-70U9e2sOIcEz_PH&status=&notStatus=')
        res = self.httpx_client.get(url=self.endpoint_task, params=obj_filter({'id': id_list ,'status': status, 'notStatus': notStatus})) # type: ignore
        json = check_response_and_return_data(res)
        return GetTaskList_Response(**json)
    
    async def async_get_task_list(self,id_list: List[str], status: List[TASK_STATUS] | None = None, notStatus: List[TASK_STATUS] | None = None) -> GetTaskList_Response:
        """Async implementation of get_task_list."""
        res = await self.async_httpx_client.get(url=self.endpoint_task, params=obj_filter({'id': id_list ,'status': status, 'notStatus': notStatus})) # type: ignore
        json = check_response_and_return_data(res)
        return GetTaskList_Response(**json)

    def create_a_task_from_resolved_id(self, rid: str, opt: CreateTask_DownloadOpt | None = None) -> CreateATask_Response:
        """receive CreateATask_fromResolvedId object as paramter. see src\gospeed_api\models\create_a_task.py for detail return data structure."""
        param = CreateATask_fromResolvedId(rid=rid, opt=opt)
        res = self.httpx_client.post(url=self.endpoint_task, json=param.model_dump())
        json = check_response_and_return_data(res)
        return CreateATask_Response(**json)
    
    async def async_create_a_task_from_resolved_id(self, rid: str, opt: CreateTask_DownloadOpt | None = None) -> CreateATask_Response:
        """receive CreateATask_fromResolvedId object as paramter. see src\gospeed_api\models\create_a_task.py for detail return data structure."""
        param = CreateATask_fromResolvedId(rid=rid, opt=opt)
        res = await self.async_httpx_client.post(url=self.endpoint_task, json=param.model_dump())
        json = check_response_and_return_data(res)
        return CreateATask_Response(**json) 

    def create_a_task_from_url(self, url: str, extra: Request_Extra_Opt | None = None, labels: Dict[str, str] | None = None, opt: CreateTask_DownloadOpt | None = None) -> CreateATask_Response:
        """Directly create a task instead of resolve it's information first."""
        param = CreateATask_FromUrl(req=ResolveRequest(url=url, extra=extra, labels=labels), opt=opt)
        res = self.httpx_client.post(self.endpoint_task, json=param.model_dump())
        json = check_response_and_return_data(res)
        return CreateATask_Response(**json)
    
    async def async_create_a_task_from_url(self, url: str, extra: Request_Extra_Opt | None = None, labels: Dict[str, str] | None = None, opt: CreateTask_DownloadOpt | None = None) -> CreateATask_Response:
        """Directly create a task instead of resolve it's information first."""
        param = CreateATask_FromUrl(req=ResolveRequest(url=url, extra=extra, labels=labels), opt=opt)
        res = await self.async_httpx_client.post(self.endpoint_task, json=param.model_dump())
        json = check_response_and_return_data(res)
        return CreateATask_Response(**json)

    def delete_tasks(self, id_list: List[str] | None = None, status: List[TASK_STATUS] | None = None, notStatus: List[TASK_STATUS] | None = None, force: bool = False) -> DeleteTasks_Response:
        """Delete tasks according to specified status."""
        query_paramter = DeleteTasks_Request(id=id_list, status=status, notStatus=notStatus, force=force)
        res = self.httpx_client.delete(self.endpoint_task, params=obj_filter(query_paramter.model_dump()))
        json = check_response_and_return_data(res)
        return DeleteTasks_Response(**json)

    async def async_delete_tasks(self, id_list: List[str] | None = None, status: List[TASK_STATUS] | None = None, notStatus: List[TASK_STATUS] | None = None, force: bool = False) -> DeleteTasks_Response:
        """Delete tasks according to specified status."""
        query_paramter = DeleteTasks_Request(id=id_list, status=status, notStatus=notStatus, force=force)
        res = await self.async_httpx_client.delete(self.endpoint_task, params=obj_filter(query_paramter.model_dump()))
        json = check_response_and_return_data(res)
        return DeleteTasks_Response(**json)

    def create_a_batch_of_tasks(self, urls: List[str], opt: CreateTask_DownloadOpt | None = None) -> CreateABatchOfTasks_Response:
        """Create multiple tasks at once."""
        reqs = [TaskUrl(url=url) for url in urls]
        data = CreateABatchOfTasks(reqs=reqs, opt=opt)
        res = self.httpx_client.post(self.endpoint_task_batch, json=data.model_dump())
        json = check_response_and_return_data(res)
        return CreateABatchOfTasks_Response(**json)
    
    async def async_create_a_batch_of_tasks(self, urls: List[str], opt: CreateTask_DownloadOpt | None = None) -> CreateABatchOfTasks_Response:
        """Create multiple tasks at once."""
        reqs = [TaskUrl(url=url) for url in urls]
        data = CreateABatchOfTasks(reqs=reqs, opt=opt)
        res = await self.async_httpx_client.post(self.endpoint_task_batch, json=data.model_dump())
        json = check_response_and_return_data(res)
        return CreateABatchOfTasks_Response(**json)

    def get_task_info(self, rid: str) -> GetTaskInfo_Response:
        """Get a task info from it's id."""
        res = self.httpx_client.get(url=my_url_join(self.endpoint_task, rid))
        json = check_response_and_return_data(res)
        return GetTaskInfo_Response(**json)
    
    async def async_get_task_info(self, rid: str) -> GetTaskInfo_Response:
        """Get a task info from it's id."""
        res = await self.async_httpx_client.get(url=my_url_join(self.endpoint_task, rid))
        json = check_response_and_return_data(res)
        return GetTaskInfo_Response(**json)

    def delete_a_task(self, rid: str, force: bool = False) -> DeleteATask_Response:
        """Delete a task by specify it's id, force if true will delete the file also."""
        res = self.httpx_client.delete(url=my_url_join(self.endpoint_task, rid), params=obj_filter({'force': force}))
        json = check_response_and_return_data(res)
        return DeleteATask_Response(**json)
    
    async def async_delete_a_task(self, rid: str, force: bool = False) -> DeleteATask_Response:
        """Delete a task by specify it's id, force if true will delete the file also."""
        res = await self.async_httpx_client.delete(url=my_url_join(self.endpoint_task, rid), params=obj_filter({'force': force}))
        json = check_response_and_return_data(res)
        return DeleteATask_Response(**json)
    
    def get_task_stats(self, rid: str) -> GetTaskStats_Response:
        """get BT task stats"""
        res = self.httpx_client.get(my_url_join(my_url_join(self.endpoint_info, rid), 'stats'))
        json = check_response_and_return_data(res)
        return GetTaskStats_Response(**json)
    
    async def async_get_task_stats(self, rid: str) -> GetTaskStats_Response:
        """get BT task stats"""
        res = await self.async_httpx_client.get(my_url_join(my_url_join(self.endpoint_info, rid), 'stats'))
        json = check_response_and_return_data(res)
        return GetTaskStats_Response(**json)

    def pause_a_task(self, rid: str) -> PauseATask_Response:
        """Pause a task download according to task id."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'pause')
        res = self.httpx_client.put(url=url)
        json = check_response_and_return_data(res)
        return PauseATask_Response(**json)
    
    async def async_pause_a_task(self, rid: str) -> PauseATask_Response:
        """Pause a task download according to task id."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'pause')
        res = await self.async_httpx_client.put(url=url)
        json = check_response_and_return_data(res)
        return PauseATask_Response(**json)

    def pause_all_tasks(self) -> PauseAllTasks_Response:
        """Palse every tasks inside Gospeed downloader."""
        res = self.httpx_client.put(url=self.endpoint_tasks_pause)
        json = check_response_and_return_data(res)
        return PauseAllTasks_Response(**json)

    async def async_pause_all_tasks(self) -> PauseAllTasks_Response:
        """Palse every tasks inside Gospeed downloader."""
        res = await self.async_httpx_client.put(url=self.endpoint_tasks_pause)
        json = check_response_and_return_data(res)
        return PauseAllTasks_Response(**json)

    def continue_a_task(self, rid: str) -> ContinueATask_Response:
        """Continue a stop task according to task id."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'continue')
        res = self.httpx_client.put(url=url)
        json = check_response_and_return_data(res)
        return ContinueATask_Response(**json)
    
    async def async_continue_a_task(self, rid: str) -> ContinueATask_Response:
        """Continue a stop task according to task id."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'continue')
        res = await self.async_httpx_client.put(url=url)
        json = check_response_and_return_data(res)
        return ContinueATask_Response(**json)

    def continue_all_tasks(self) -> ContinueAllTasks_Response:
        """Continue every tasks inside Gospeed downloader."""
        res = self.httpx_client.put(url=self.endpoint_tasks_continue)
        json = check_response_and_return_data(res)
        return ContinueAllTasks_Response(**json)

    async def async_continue_all_tasks(self) -> ContinueAllTasks_Response:
        """Continue every tasks inside Gospeed downloader."""
        res = await self.async_httpx_client.put(url=self.endpoint_tasks_continue)
        json = check_response_and_return_data(res)
        return ContinueAllTasks_Response(**json)
