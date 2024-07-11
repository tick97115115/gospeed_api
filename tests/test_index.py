from gospeed_api.index import GospeedClient, AsyncGospeedClient
import tempfile
import time
import anyio


# For example showcase, I will write import statement inside test method.
# pylint: disable=C0415
# prevent warning of non-top import statement

class TestClassGospeedClientInstance:
    """Initialize object with api address."""
    client = GospeedClient('http://127.0.0.1:9999/')

    def test_get_server_info(self):
        """test get server info function"""
        from gospeed_api.models.get_server_info import GetServerInfo_Response

        res: GetServerInfo_Response = self.client.get_server_info()
        # If response.code property == 0, it means everything working fine.
        assert res.code == 0
  
    def test_get_task_list(self):
        """Retrive all tasks info those corresponding to specified status"""
        from gospeed_api.models.get_task_list import GetTaskList_Response
        from gospeed_api.models import TASK_STATUS

        data: GetTaskList_Response = self.client.get_task_list(status={TASK_STATUS.DONE}) 
        # This method Receive a Set[Task_STATUS] as input, you could specify different status inside like:
        # self.client.get_task_list({TASK_STATUS.DONE, TASK_STATUS.PAUSE}) to retrive multiple tasks info those have corresponding status.
        # 
        # If you want get every task info, just ignore status paramter, 
        # like: self.client.get_task_list()
        assert data.code == 0

    def test_create_a_task_and_get_task_info(self):
        """A comprehensive test. resolve_request, create task, check task info and delete task finally."""
        from gospeed_api.models import CreateTask_DownloadOpt, TASK_STATUS
        from gospeed_api.models.create_a_task import CreateATask_fromResolvedId, CreateATask_Response
        from gospeed_api.models.get_task_info import GetTaskInfo_Response
        from gospeed_api.models.resolve_a_request import ResolveRequest

        # resolve a resource request link
        resolve_request_param = ResolveRequest(url="https://example.com/index.html")
        resolvedInfo = self.client.resolve_a_request(param=resolve_request_param)
        # create a download task by resolved info id
        create_a_task_by_id_opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        create_a_task_by_id_param = CreateATask_fromResolvedId(rid=resolvedInfo.data.id, opt=create_a_task_by_id_opt)
        # get task object info and task id
        task: CreateATask_Response = self.client.create_a_task_from_resolved_id(param=create_a_task_by_id_param)
        rid = task.data
        # use get_task_info method, the 'res' property inside Task_Meta Class will return None
        task_info: GetTaskInfo_Response = self.client.get_task_info(rid=rid)
        assert task_info.code == 0
        # Retrive task info and check task status
        while True:
            time.sleep(2)
            task_info: GetTaskInfo_Response = self.client.get_task_info(rid=rid)
            if (task_info.data.status == TASK_STATUS.DONE):
                break
        # Detele task, force=True means delete file also.
        self.client.delete_a_task(rid=task_info.data.id, force=True)

    def test_resolve_a_request_create_a_task_from_resolved_info_and_delete_the_task(self):
        from gospeed_api.models.resolve_a_request import ResolveRequest
        from gospeed_api.models.create_a_task import CreateTask_DownloadOpt, CreateATask_fromResolvedId
        from gospeed_api.models import TASK_STATUS

        # Resolve resource
        id_resolve_response = self.client.resolve_a_request(ResolveRequest(url="https://example.com/index.html"))
        assert id_resolve_response.code == 0
        
        # Create download task from resolved id
        rid = id_resolve_response.data.id
        filename = id_resolve_response.data.res.files[0].name
        opt = CreateTask_DownloadOpt(name=filename, path=tempfile.gettempdir())
        task = self.client.create_a_task_from_resolved_id(CreateATask_fromResolvedId(rid=rid, opt=opt))
        assert task.code == 0
        # print(f"task_id: {task.data}") # When create single task, the returned object's data property is task id!
        
        # Get task info and checking status
        while True:
            time.sleep(2)
            task_info = self.client.get_task_info(rid=task.data)
            if (task_info.data.status == TASK_STATUS.DONE):
                break
        # Delete task
        delete_response = self.client.delete_a_task(rid=task.data, force=True)
        assert delete_response.code == 0
    
    def test_create_a_request_from_url(self):
        from gospeed_api.models.create_a_task import CreateTask_DownloadOpt, CreateATask_fromUrl
        from gospeed_api.models import ResolveRequest_Response_Res_File_Req, TASK_STATUS

        # create download task from url
        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        req = ResolveRequest_Response_Res_File_Req(url='https://example.com/index.html')
        data = CreateATask_fromUrl(req=req, opt=opt)
        task = self.client.create_a_task_from_url(param=data)
        assert task.code == 0
        # print(f"task_id: {task.data}") # task id
        # delete task
        while True:
            time.sleep(2)
            task_info = self.client.get_task_info(rid=task.data)
            if (task_info.data.status == TASK_STATUS.DONE):
                break
        delete_response = self.client.delete_a_task(rid=task.data, force=True)
        assert delete_response.code == 0

    def test_create_and_delete_a_batch_of_tasks(self):
        from gospeed_api.models.create_a_batch_of_tasks import TaskUrl, CreateABatchOfTasks, CreateABatchOfTasks_Response
        from gospeed_api.models.create_a_task import CreateTask_DownloadOpt
        from gospeed_api.models.get_task_info import GetTaskInfo_Response
        from gospeed_api.models import TASK_STATUS
        from gospeed_api.models.delete_a_task import DeleteATask_Response

        # Define two target urls.
        url1 = TaskUrl(url='https://example.com/index.html')
        url2 = TaskUrl(url='https://example.com/index.html')
        
        # define download opt
        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        # Create download task
        tasks = CreateABatchOfTasks(reqs=[url1, url2], opt=opt)
        res_data: CreateABatchOfTasks_Response = self.client.create_a_batch_of_tasks(data=tasks)
        assert res_data.code == 0

        while True:
            time.sleep(2)
            task1_info: GetTaskInfo_Response = self.client.get_task_info(res_data.data[0])
            task2_info: GetTaskInfo_Response = self.client.get_task_info(res_data.data[1])
            # check task status and delete them
            if (task1_info.data.status == TASK_STATUS.DONE and task2_info.data.status == TASK_STATUS.DONE):
                task1_delete_res: DeleteATask_Response = self.client.delete_a_task(rid=res_data.data[0])
                task2_delete_res: DeleteATask_Response = self.client.delete_a_task(rid=res_data.data[1])
                # For avoid test exception, in here I delete them one by one, please take much care when use this function.
                # delete all exists tasks, like below: 
                # self.client.delete_tasks(status={TASK_STATUS.DONE, TASK_STATUS.ERROR}, force=True)
                assert task1_delete_res.code == 0
                assert task2_delete_res.code == 0
                break

    def test_pause_and_continue_task(self):
        """test pause one/every and continue one/every task function."""
        # http://speedtest.tele2.net/ used for speed test by download big file.
        # http://speedtest.tele2.net/100MB.zip this is what I used.
        from gospeed_api.models import ResolveRequest_Response_Res_File_Req
        from gospeed_api.models import TASK_STATUS, CreateTask_DownloadOpt
        from gospeed_api.models.create_a_task import CreateATask_fromUrl

        # create a task
        req = ResolveRequest_Response_Res_File_Req(url="http://speedtest.tele2.net/100MB.zip")
        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        data = CreateATask_fromUrl(req=req, opt=opt)
        task = self.client.create_a_task_from_url(data)
        assert task.code == 0
        time.sleep(1)
        task_rid = task.data
        res = self.client.get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.RUNNING

        # pause a task
        time.sleep(2)
        res = self.client.pause_a_task(rid=task_rid)
        assert res.code == 0
        time.sleep(1)
        res = self.client.get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.PAUSE

        #continue a task
        time.sleep(2)
        res = self.client.continue_a_task(rid=task_rid)
        assert res.code == 0
        time.sleep(1)
        res = self.client.get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.RUNNING

        # pause all tasks
        time.sleep(2)
        res = self.client.pause_all_tasks()
        assert res.code == 0
        time.sleep(1)
        res = self.client.get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.PAUSE

        # continue all tasks
        time.sleep(2)
        res = self.client.continue_all_tasks()
        assert res.code == 0
        time.sleep(1)
        res = self.client.get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.RUNNING

        # delete task
        res = self.client.delete_a_task(rid=task_rid, force=True)
        assert res.code == 0


import pytest
pytestmark = pytest.mark.anyio
class TestClassAsyncGospeedClientInstance:
    """Initialize object with api address."""
    async_client = AsyncGospeedClient('http://127.0.0.1:9999/')

    async def test_async_get_server_info(self):
        """test async_get_server_info method, no much difference with sync version."""
        from gospeed_api.models.get_server_info import GetServerInfo_Response
        
        res: GetServerInfo_Response = await self.async_client.async_get_server_info()
        assert res.code == 0

    async def test_async_get_task_list(self):
        """test async_get_task_list method, no much difference with sync version."""
        from gospeed_api.models.get_task_list import GetTaskList_Response
        from gospeed_api.models import TASK_STATUS
        
        data: GetTaskList_Response = await self.async_client.async_get_task_list(status={TASK_STATUS.DONE})
        assert data.code == 0

    async def test_async_create_a_task_and_get_task_info(self):
        """A comprehensive test. resolve_request, create task, check task info and delete task finally."""
        from gospeed_api.models import CreateTask_DownloadOpt, TASK_STATUS
        from gospeed_api.models.create_a_task import CreateATask_fromResolvedId, CreateATask_Response
        from gospeed_api.models.get_task_info import GetTaskInfo_Response
        from gospeed_api.models.resolve_a_request import ResolveRequest

        # resolve a resource request link
        resolve_request_param = ResolveRequest(url="https://example.com/index.html")
        resolved_info = await self.async_client.async_resolve_a_request(param=resolve_request_param)
        # create a download task by resolved info id
        create_a_task_by_id_opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        create_a_task_by_id_param = CreateATask_fromResolvedId(rid=resolved_info.data.id, opt=create_a_task_by_id_opt)
        # get task object info and task id
        task: CreateATask_Response = await self.async_client.async_create_a_task_from_resolved_id(param=create_a_task_by_id_param)
        rid = task.data
        # use get_task_info method, the 'res' property inside Task_Meta Class will return None
        task_info: GetTaskInfo_Response = await self.async_client.async_get_task_info(rid=rid)
        assert task_info.code == 0
        # Retrive task info and check task status
        while True:
            anyio.sleep(2)
            task_info: GetTaskInfo_Response = await self.async_client.async_get_task_info(rid=rid)
            if (task_info.data.status == TASK_STATUS.DONE):
                break
        # Detele task, force=True means delete file also.
        await self.async_client.async_delete_a_task(rid=task_info.data.id, force=True)

    async def test_async_resolve_a_request_create_a_task_from_resolved_info_and_delete_the_task(self):
        """A comprehensive test. resolve_request, create task, check task info and delete task finally."""
        from gospeed_api.models.resolve_a_request import ResolveRequest
        from gospeed_api.models.create_a_task import CreateTask_DownloadOpt, CreateATask_fromResolvedId
        from gospeed_api.models import TASK_STATUS

        # Resolve resource
        id_resolve_response = await self.async_client.async_resolve_a_request(ResolveRequest(url="https://example.com/index.html"))
        assert id_resolve_response.code == 0
        
        # Create download task from resolved id
        rid = id_resolve_response.data.id
        filename = id_resolve_response.data.res.files[0].name
        opt = CreateTask_DownloadOpt(name=filename, path=tempfile.gettempdir())
        task = await self.async_client.async_create_a_task_from_resolved_id(CreateATask_fromResolvedId(rid=rid, opt=opt))
        assert task.code == 0
        # print(f"task_id: {task.data}") # When create single task, the returned object's data property is task id!
        
        # Get task info and checking status
        while True:
            anyio.sleep(2)
            task_info = await self.async_client.async_get_task_info(rid=task.data)
            if (task_info.data.status == TASK_STATUS.DONE):
                break
        # Delete task
        delete_response = await self.async_client.async_delete_a_task(rid=task.data, force=True)
        assert delete_response.code == 0

    async def test_async_create_a_request_from_url(self):
        """A comprehensive test. resolve_request, create task, check task info and delete task finally."""
        from gospeed_api.models.create_a_task import CreateTask_DownloadOpt, CreateATask_fromUrl
        from gospeed_api.models import ResolveRequest_Response_Res_File_Req, TASK_STATUS

        # create download task from url
        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        req = ResolveRequest_Response_Res_File_Req(url='https://example.com/index.html')
        data = CreateATask_fromUrl(req=req, opt=opt)
        task = await self.async_client.async_create_a_task_from_url(param=data)
        assert task.code == 0
        # print(f"task_id: {task.data}") # task id
        # delete task
        while True:
            anyio.sleep(2)
            task_info = await self.async_client.async_get_task_info(rid=task.data)
            if (task_info.data.status == TASK_STATUS.DONE):
                break
        delete_response = await self.async_client.async_delete_a_task(rid=task.data, force=True)
        assert delete_response.code == 0

    async def test_async_create_and_delete_a_batch_of_tasks(self):
        """A comprehensive test. resolve_request, create task, check task info and delete task finally."""
        from gospeed_api.models.create_a_batch_of_tasks import TaskUrl, CreateABatchOfTasks, CreateABatchOfTasks_Response
        from gospeed_api.models.create_a_task import CreateTask_DownloadOpt
        from gospeed_api.models.get_task_info import GetTaskInfo_Response
        from gospeed_api.models import TASK_STATUS
        from gospeed_api.models.delete_a_task import DeleteATask_Response

        # Define two target urls.
        url1 = TaskUrl(url='https://example.com/index.html')
        url2 = TaskUrl(url='https://example.com/index.html')
        
        # define download opt
        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        # Create download task
        tasks = CreateABatchOfTasks(reqs=[url1, url2], opt=opt)
        res_data: CreateABatchOfTasks_Response = await self.async_client.async_create_a_batch_of_tasks(data=tasks)
        assert res_data.code == 0

        while True:
            anyio.sleep(2)
            task1_info: GetTaskInfo_Response = await self.async_client.async_get_task_info(res_data.data[0])
            task2_info: GetTaskInfo_Response = await self.async_client.async_get_task_info(res_data.data[1])
            if (task1_info.data.status == TASK_STATUS.DONE and task2_info.data.status == TASK_STATUS.DONE):
                task1_delete_res: DeleteATask_Response = await self.async_client.async_delete_a_task(rid=res_data.data[0])
                task2_delete_res: DeleteATask_Response = await self.async_client.async_delete_a_task(rid=res_data.data[1])
                # For avoid test exception, in here I delete them one by one, please take much care when use this function.
                # delete all exists tasks, like below: 
                # await self.async_client.async_delete_tasks(status={TASK_STATUS.DONE, TASK_STATUS.ERROR}, force=True)
                assert task1_delete_res.code == 0
                assert task2_delete_res.code == 0
                break
    
    async def test_async_pause_and_continue_task(self):
        """test pause one/every and continue one/every task function."""
        # http://speedtest.tele2.net/ used for speed test by download big file.
        # http://speedtest.tele2.net/100MB.zip this is what I used.
        from gospeed_api.models import ResolveRequest_Response_Res_File_Req
        from gospeed_api.models import TASK_STATUS, CreateTask_DownloadOpt
        from gospeed_api.models.create_a_task import CreateATask_fromUrl

        # create a task
        req = ResolveRequest_Response_Res_File_Req(url="http://speedtest.tele2.net/100MB.zip")
        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        data = CreateATask_fromUrl(req=req, opt=opt)
        task = await self.async_client.async_create_a_task_from_url(data)
        assert task.code == 0
        anyio.sleep(1)
        task_rid = task.data
        res = await self.async_client.async_get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.RUNNING

        # pause a task
        anyio.sleep(2)
        res = await self.async_client.async_pause_a_task(rid=task_rid)
        assert res.code == 0
        anyio.sleep(1)
        res = await self.async_client.async_get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.PAUSE

        #continue a task
        anyio.sleep(2)
        res = await self.async_client.async_continue_a_task(rid=task_rid)
        assert res.code == 0
        anyio.sleep(1)
        res = await self.async_client.async_get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.RUNNING

        # pause all tasks
        anyio.sleep(2)
        res = await self.async_client.async_pause_all_tasks()
        assert res.code == 0
        anyio.sleep(1)
        res = await self.async_client.async_get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.PAUSE

        # continue all tasks
        anyio.sleep(2)
        res = await self.async_client.async_continue_all_tasks()
        assert res.code == 0
        anyio.sleep(1)
        res = await self.async_client.async_get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.RUNNING

        # delete task
        res = await self.async_client.async_delete_a_task(rid=task_rid, force=True)
        assert res.code == 0

class TestClassGospeedClientInstance_DeleteAllTasks:
    """Initialize object with api address."""
    client = GospeedClient('http://127.0.0.1:9999/')

    def test_delete_all_tasks(self):
        """test delete teaks method"""
        # http://speedtest.tele2.net/100MB.zip this is what I used.
        from gospeed_api.models import ResolveRequest_Response_Res_File_Req
        from gospeed_api.models import TASK_STATUS, CreateTask_DownloadOpt
        from gospeed_api.models.create_a_task import CreateATask_fromUrl

        # create a task
        req = ResolveRequest_Response_Res_File_Req(url="http://speedtest.tele2.net/100MB.zip")
        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        data = CreateATask_fromUrl(req=req, opt=opt)
        task = self.client.create_a_task_from_url(data)
        assert task.code == 0
        time.sleep(1)
        task_rid = task.data
        res = self.client.get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.RUNNING

        # invoke delete all tasks api
        self.client.delete_tasks(force=True) # leave status param to None, means delete all tasks inside downloader no matter what status it is.
        time.sleep(1)

        # check if have any task exists
        res = self.client.get_task_list()
        assert len(res.data) == 0

class TestClassAsyncGospeedClientInstance_DeleteAllTasks:
    """Initialize object with api address."""
    async_client = AsyncGospeedClient('http://127.0.0.1:9999/')

    async def test_async_delete_all_tasks(self):
        """test async delete teaks method"""
        # http://speedtest.tele2.net/100MB.zip this is what I used.
        from gospeed_api.models import ResolveRequest_Response_Res_File_Req
        from gospeed_api.models import TASK_STATUS, CreateTask_DownloadOpt
        from gospeed_api.models.create_a_task import CreateATask_fromUrl

        # create a task
        req = ResolveRequest_Response_Res_File_Req(url="http://speedtest.tele2.net/100MB.zip")
        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        data = CreateATask_fromUrl(req=req, opt=opt)
        task = await self.async_client.async_create_a_task_from_url(data)
        assert task.code == 0
        anyio.sleep(1)
        task_rid = task.data
        res = self.async_client.get_task_info(rid=task_rid)
        assert res.data.status == TASK_STATUS.RUNNING

        # invoke delete all tasks api
        await self.async_client.async_delete_tasks(force=True) # leave status param to None, means delete all tasks inside downloader no matter what status it is.
        anyio.sleep(1)

        # check if have any task exists
        res = await self.async_client.async_get_task_list()
        assert len(res.data) == 0
