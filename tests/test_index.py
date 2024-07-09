from gospeed_api.index import GospeedClient
import tempfile
import time

# For example showcase, I will write import statement inside test method.
# pylint: disable=C0415
# prevent warning of non-top import statement

class TestClassGospeedClientInstance:
    """Initialize object with api address."""
    client = GospeedClient('http://127.0.0.1:9999/')

    def test_get_server_info(self):
        from gospeed_api.models.get_server_info import GetServerInfo_Response

        res: GetServerInfo_Response = self.client.get_server_info()
        assert res.code == 0
  
    def test_get_task_list(self):
        from gospeed_api.models.get_task_list import GetTaskList_Response
        from gospeed_api.models import TASK_STATUS

        data: GetTaskList_Response = self.client.get_task_list({TASK_STATUS.DONE})
        assert data.code == 0

    def test_get_task_info(self):
        from gospeed_api.models import CreateTask_DownloadOpt, ResolveRequest_Response_Res_File_Req, TASK_STATUS
        from gospeed_api.models.create_a_task import CreateATask_fromUrl, CreateATask_Response
        from gospeed_api.models.get_task_info import GetTaskInfo_Response

        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        req = ResolveRequest_Response_Res_File_Req(url="https://example.com/index.html")
        data = CreateATask_fromUrl(req=req, opt=opt)
        task: CreateATask_Response = self.client.create_a_task_from_url(param=data)
        rid = task.data
        # get_task_info in this case, the 'res' property will return None
        task_info = self.client.get_task_info(rid=rid)
        assert task_info.code == 0
        # delete task
        while True:
            time.sleep(2)
            task_info: GetTaskInfo_Response = self.client.get_task_info(rid=rid)
            if (task_info.data.status == TASK_STATUS.DONE):
                break
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

        url1 = TaskUrl(url='https://example.com/index.html')
        url2 = TaskUrl(url='https://example.com/index.html')

        opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
        tasks = CreateABatchOfTasks(reqs=[url1, url2], opt=opt)
        res_data: CreateABatchOfTasks_Response = self.client.create_a_batch_of_tasks(data=tasks)
        assert res_data.code == 0

        while True:
            time.sleep(2)
            task1_info: GetTaskInfo_Response = self.client.get_task_info(res_data.data[0])
            task2_info: GetTaskInfo_Response = self.client.get_task_info(res_data.data[1])
            if (task1_info.data.status == TASK_STATUS.DONE and task2_info.data.status == TASK_STATUS.DONE):
                task1_delete_res: DeleteATask_Response = self.client.delete_a_task(rid=res_data.data[0])
                task2_delete_res: DeleteATask_Response = self.client.delete_a_task(rid=res_data.data[1])
                assert task1_delete_res.code == 0
                assert task2_delete_res.code == 0
                break

    def test_pause_and_continue_task(self):
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
