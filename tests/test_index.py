from src.gospeed_api.index import GospeedAPI
from src.gospeed_api.models import TASK_STATUS
from src.gospeed_api.models.create_a_task import CreateATask_Response
import time
import anyio

import pytest
pytestmark = pytest.mark.anyio

# For example showcase, I will write import statement inside test method.
# For simplify, see how tests running in TestGospeedAPI_Sync class will be enough to capture the usage,
# cause use async functions have not much difference. (Just add "await" keyword before every async function.)

@pytest.fixture
def gopeed_api():
    return GospeedAPI("http://127.0.0.1:9999")

class TestGospeedAPI_Sync:
    def test_how_to_CRUD_singel_Gopeed_task(self, gopeed_api: GospeedAPI):
        # create task and get task_id
        task_0 = gopeed_api.create_a_task_from_url(url="http://speedtest.tele2.net/100MB.zip")
        task_0.task_id

        time.sleep(1)

        # fetch task status
        task_0_status = gopeed_api.get_task_info(rid=task_0.task_id)
        assert task_0_status.task_info.status == TASK_STATUS.RUNNING

        # pause a task
        task_0_res_0 = gopeed_api.pause_a_task(task_0.task_id)
        assert task_0_res_0.code == 0 # success

        time.sleep(1)

        # continue a task
        task_0_res_1 = gopeed_api.continue_a_task(task_0.task_id)
        assert task_0_res_1.code == 0 # success

        # delete a task
        task_0_res_2 = gopeed_api.delete_a_task(task_0.task_id, force=True) # force means to delete the task's file too
        assert task_0_res_2.code == 0 # success
    
    def test_how_to_CRUD_multiple_Gopeed_tasks(self, gopeed_api: GospeedAPI):
        # create a bunch of tasks
        urls = [
            'http://speedtest.tele2.net/1MB.zip',
            'http://speedtest.tele2.net/10MB.zip',
            'http://speedtest.tele2.net/100MB.zip',
            'http://speedtest.tele2.net/1GB.zip'
        ]
        tasks = gopeed_api.create_a_batch_of_tasks(urls=urls)

        time.sleep(1)

        # fetch status of multiple tasks
        task_info_list = gopeed_api.get_task_list(tasks.id_list)
        for task in task_info_list.data:
            assert task.meta.req.url in urls
        task_info_list = gopeed_api.get_task_list(tasks.id_list)
        assert len(task_info_list.data) == 4

        # pause all tasks
        gopeed_api.pause_all_tasks()

        time.sleep(1)

        def check_pause_status():
            # fetch status of multiple tasks
            task_info_list = gopeed_api.get_task_list(tasks.id_list)
            for task in task_info_list.data:
                if (task.status == TASK_STATUS.PAUSE):
                    return
            raise Exception("pause failed")
        check_pause_status()

        # continue all tasks
        gopeed_api.continue_all_tasks()

        time.sleep(1)

        def check_continue_status():
            # fetch status of multiple tasks
            task_info_list = gopeed_api.get_task_list(tasks.id_list)
            for task in task_info_list.data:
                if (task.status == TASK_STATUS.RUNNING):
                    return
            raise Exception("continue failed")
        check_continue_status()

        # delete tasks
        gopeed_api.delete_tasks(tasks.id_list)

class TestGospeedAPI_Async:
    async def test_how_to_CRUD_singel_Gopeed_task(self, gopeed_api: GospeedAPI):
        # create task and get task_id
        task_0 = await gopeed_api.async_create_a_task_from_url(url="http://speedtest.tele2.net/100MB.zip")
        task_0.task_id

        await anyio.sleep(1)

        # fetch task status
        task_0_status = await gopeed_api.async_get_task_info(rid=task_0.task_id)
        assert task_0_status.task_info.status == TASK_STATUS.RUNNING

        # pause a task
        task_0_res_0 = await gopeed_api.async_pause_a_task(task_0.task_id)
        assert task_0_res_0.code == 0 # success

        await anyio.sleep(1)

        # continue a task
        task_0_res_1 = await gopeed_api.async_continue_a_task(task_0.task_id)
        assert task_0_res_1.code == 0 # success

        # delete a task
        task_0_res_2 = await gopeed_api.async_delete_a_task(task_0.task_id, force=True) # force means to delete the task's file too
        assert task_0_res_2.code == 0 # success
    
    async def test_how_to_CRUD_multiple_Gopeed_tasks(self, gopeed_api: GospeedAPI):
        # create a bunch of tasks
        urls = [
            'http://speedtest.tele2.net/1MB.zip',
            'http://speedtest.tele2.net/10MB.zip',
            'http://speedtest.tele2.net/100MB.zip',
            'http://speedtest.tele2.net/1GB.zip'
        ]
        tasks = await gopeed_api.async_create_a_batch_of_tasks(urls=urls)

        await anyio.sleep(1)

        # fetch status of multiple tasks
        task_info_list = await gopeed_api.async_get_task_list(tasks.id_list)
        for task in task_info_list.data:
            assert task.meta.req.url in urls
        task_info_list = await gopeed_api.async_get_task_list(tasks.id_list)
        assert len(task_info_list.data) == 4

        # pause all tasks
        await gopeed_api.async_pause_all_tasks()

        await anyio.sleep(1)

        async def async_check_pause_status():
            # fetch status of multiple tasks
            task_info_list = await gopeed_api.async_get_task_list(tasks.id_list)
            for task in task_info_list.data:
                if (task.status == TASK_STATUS.PAUSE):
                    return
            raise Exception("pause failed")
        await async_check_pause_status()

        # continue all tasks
        await gopeed_api.async_continue_all_tasks()

        await anyio.sleep(1)

        async def async_check_continue_status():
            # fetch status of multiple tasks
            task_info_list = await gopeed_api.async_get_task_list(tasks.id_list)
            for task in task_info_list.data:
                if (task.status == TASK_STATUS.RUNNING):
                    return
            raise Exception("continue failed")
        await async_check_continue_status()

        # delete tasks
        await gopeed_api.async_delete_tasks(tasks.id_list)

def test_exception():
    res = {'code': 1, 'msg': 'test', 'data': 'test data'}
    res = CreateATask_Response(**res)
    res.raise_error()