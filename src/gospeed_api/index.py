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
import requests
from urllib.parse import urljoin
from typing import Set
from .models import TASK_STATUS

def my_url_join(first: str, last: str) -> str:
    """Checking slash symbol between url and path string."""
    if (first[-1] != '/' and last[0] != '/'):
        first = first + '/'
    return str(urljoin(first, last))

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
        res = requests.get(url=self.endpoint_info)
        if res.status_code == 200:
            json = res.json()
            return GetServerInfo_Response(**json)
        else:
            res.raise_for_status()
            return None

    def resolve_a_request(self, param: ResolveRequest) -> ResolveRequest_Response:
        """resolve request link and return ResolveRequest_Response data model object."""
        res = requests.post(url=self.endpoint_resolve, data=param.model_dump_json(), headers={"content-type": "application/json", "accept": "application/json"})
        if res.status_code == 200:
            json = res.json()
            return ResolveRequest_Response(**json)
        else:
            res.raise_for_status()
            return None

    def get_task_list(self, status: Set[TASK_STATUS]) -> GetTaskList_Response:
        """Get all tasks according to specified status."""
        res = requests.get(url=self.endpoint_task, params={'status': list(status)}, headers={'accept': 'application/json'})
        if res.status_code == 200:
            json = res.json()
            return GetTaskList_Response(**json)
        else:
            res.raise_for_status()
            return None

    def create_a_task_from_resolved_id(self, param: CreateATask_fromResolvedId) -> CreateATask_Response:
        r"""receive CreateATask_fromResolvedId object as paramter. see src\gospeed_api\models\create_a_task.py for detail return data structure."""
        res = requests.post(url=self.endpoint_task, headers={"accept": "application/json", "content-type": "application/json"}, data=param.model_dump_json())
        if res.status_code == 200:
            json = res.json()
            return CreateATask_Response(**json)
        else:
            res.raise_for_status()
            return None

    def create_a_task_from_url(self, param: CreateATask_fromUrl) -> CreateATask_Response:
        """Directly create a task instead of resolve it's information first."""
        res = requests.post(self.endpoint_task, headers={"accept": "application/json", "content-type": "application/json"}, data=param.model_dump_json())
        if res.status_code == 200:
            json = res.json()
            return CreateATask_Response(**json)
        else:
            res.raise_for_status()
            return None

    def delete_a_task(self, rid: str, force: bool = False) -> DeleteATask_Response:
        """Delete a task by specify it's id, force if true will delete the file also."""
        res = requests.delete(url=my_url_join(self.endpoint_task, rid), params={'force': str(force).lower()})
        if res.status_code == 200:
            json = res.json()
            return DeleteATask_Response(**json)
        else:
            res.raise_for_status()
            return None

    def create_a_batch_of_tasks(self, data: CreateABatchOfTasks) -> CreateABatchOfTasks_Response:
        """Create multiple tasks at once."""
        res = requests.post(self.endpoint_task_batch, headers={"accept": "application/json", "content-type": "application/json"}, data=data.model_dump_json())
        if res.status_code == 200:
            json = res.json()
            return CreateABatchOfTasks_Response(**json)
        else:
            res.raise_for_status()
            return None

    def delete_tasks(self, status: Set[TASK_STATUS], force: bool = False) -> DeleteATask_Response:
        """Delete tasks according to specified status."""
        res = requests.delete(self.endpoint_task, params={'status': list(status), 'force': str(force).lower()})
        if res.status_code == 200:
            json = res.json()
            return DeleteATask_Response(**json)
        else:
            res.raise_for_status()
            return None

    def get_task_info(self, rid: str) -> GetTaskInfo_Response:
        """Get a task info from it's id."""
        res = requests.get(url=my_url_join(self.endpoint_task, rid), headers={"accept": "application/json"})
        if res.status_code == 200:
            json = res.json()
            return GetTaskInfo_Response(**json)
        else:
            res.raise_for_status()
            return None

    def pause_a_task(self, rid: str):
        """Pause a task download according to task id."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'pause')
        res = requests.put(url=url)
        if (res.status_code == 200):
            json = res.json()
            return PauseATask_Response(**json)
        else:
            res.raise_for_status()
            return None

    def continue_a_task(self, rid: str):
        """Continue a stop task according to task id."""
        url = my_url_join(self.endpoint_task, rid)
        url = my_url_join(url, 'continue')
        res = requests.put(url=url)
        if (res.status_code == 200):
            json = res.json()
            return ContinueATask_Response(**json)
        else:
            res.raise_for_status()
            return None

    def pause_all_tasks(self):
        """Palse every tasks inside Gospeed downloader."""
        res = requests.put(self.endpoint_tasks_pause)
        if (res.status_code == 200):
            json = res.json()
            return PauseAllTasks_Response(**json)
        else:
            res.raise_for_status()
            return None

    def continue_all_tasks(self):
        """Continue every tasks inside Gospeed downloader."""
        res = requests.put(self.endpoint_tasks_continue)
        if (res.status_code == 200):
            json = res.json()
            return ContinueAllTasks_Response(**json)
        else:
            res.raise_for_status()
            return None
