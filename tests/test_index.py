from gospeed_api.index import GospeedClient, my_url_join
from gospeed_api.models.post_resolve_a_request import ResolveRequest
from gospeed_api.models import TASK_STATUS, CreateTask_DownloadOpt, ResolveRequest_Response_Res_File_Req
from gospeed_api.models.create_a_task import CreateATask_fromResolvedId, CreateATask_fromUrl
from gospeed_api.models.create_a_batch_of_tasks import CreateABatchOfTasks, TaskUrl
import tempfile
import time
import requests

class TestClassGospeedClientInstance:
  client = GospeedClient('http://127.0.0.1:9999/')

  def test_get_server_info(self):
    res = self.client.get_server_info()
    assert res.code == 0
  
  def test_get_task_list(self):
    data = self.client.get_task_list({TASK_STATUS.DONE})
    assert data.code == 0

  def test_get_task_info(self):
    opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
    req = ResolveRequest_Response_Res_File_Req(url="https://example.com/index.html")
    data = CreateATask_fromUrl(req=req, opt=opt)
    task = self.client.create_a_task_from_url(data=data)
    rid = task.data
    # get_task_info in this case, the 'res' property will return None
    task_info = self.client.get_task_info(rid=rid)
    assert task_info.code == 0
    # delete task
    while True:
      time.sleep(2)
      task_info = self.client.get_task_info(rid=rid)
      if (task_info.data.status == TASK_STATUS.DONE):
        break
    self.client.delete_a_task(rid=task_info.data.id, force=True)

  def test_resolveRequest_createRequestFromId_and_deleteATask(self):
    # resolve resource
    id_resolve_response = self.client.resolve_a_request(ResolveRequest(url="https://example.com/index.html"))
    assert id_resolve_response.code == 0
    # create download task from resolved id
    rid = id_resolve_response.data.id
    filename = id_resolve_response.data.res.files[0].name
    opt = CreateTask_DownloadOpt(name=filename, path=tempfile.gettempdir(), )
    task = self.client.create_a_task_from_resolved_id(CreateATask_fromResolvedId(rid=rid, opt=opt))
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
    
  def test_createRequestFromUrl(self):
    # create download task from url
    opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
    req = ResolveRequest_Response_Res_File_Req(url='https://example.com/index.html')
    data = CreateATask_fromUrl(req=req, opt=opt)
    task = self.client.create_a_task_from_url(data=data)
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
    url1 = TaskUrl(url='https://example.com/index.html')
    url2 = TaskUrl(url='https://example.com/index.html')

    opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
    tasks = CreateABatchOfTasks(reqs=[url1, url2], opt=opt)
    res_data = self.client.create_a_batch_of_tasks(data=tasks)
    assert res_data.code == 0

    while True:
      time.sleep(2)
      task1_info = self.client.get_task_info(res_data.data[0])
      task2_info = self.client.get_task_info(res_data.data[1])
      if (task1_info.data.status == TASK_STATUS.DONE and task2_info.data.status == TASK_STATUS.DONE):
        task1_delete_res = self.client.delete_a_task(rid=res_data.data[0])
        task2_delete_res = self.client.delete_a_task(rid=res_data.data[1])
        assert task1_delete_res.code == 0
        assert task2_delete_res.code == 0
        break

  def test_pause_and_continue_task(self):
    # http://speedtest.tele2.net/ used for speed test by download big file.
    # http://speedtest.tele2.net/100MB.zip this is what I used.
    
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
