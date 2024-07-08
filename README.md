# gospeed_api

This project provide Gospeed downloader RestAPI full-covered interacting.

All  data model is type checked in runtime by using [Pydantic](https://docs.pydantic.dev/). 


# Usage Example

every example from test file, for more detail please see: [test_index.py](./tests/test_index.py)

## Initialize

```python
from gospeed_api.index import GospeedClient

client = GospeedClient('http://127.0.0.1:9999/')
```

## Get Server Info

```python
from gospeed_api.index import GospeedClient

client = GospeedClient('http://127.0.0.1:9999/')

data = client.get_server_info() 
# response object is "GetServerInfo_Response" 
# see src\gospeed_api\models\get_server_info.py 
# for more information.
```

## Get Task List

```python
from gospeed_api.index import GospeedClient

client = GospeedClient('http://127.0.0.1:9999/')

data = self.client.get_task_list({TASK_STATUS.DONE})
# response object is "GetTaskList_Response" 
# see src\gospeed_api\models\get_task_list.py
# for more information.
```

## Resolve resource, Create Task from resource id and delete task

```python
    # resolve resource
    id_resolve_response = self.client.resolve_a_request(ResolveRequest(url="https://example.com/index.html"))
    assert id_resolve_response.code == 0
    # create download task from resolved id
    rid = id_resolve_response.data.id
    filename = id_resolve_response.data.res.files[0].name
    opt = CreateTask_DownloadOpt(name=filename, path=tempfile.gettempdir(), )
    task = self.client.create_a_task_from_resolved_id(CreateATask_fromResolvedId(rid=rid, opt=opt))
    assert task.code == 0
    # get task info (check download status)
    while True:
      time.sleep(2)
      task_info = self.client.get_task_info(rid=task.data)
      if (task_info.data.status == TASK_STATUS.DONE):
        break
    # delete task
    delete_response = self.client.delete_a_task(rid=task.data, force=True)
    assert delete_response.code == 0
```
## Create Task from url directly

```python
    # create download task from url
    opt = CreateTask_DownloadOpt(path=tempfile.gettempdir())
    req = ResolveRequest_Response_Res_File_Req(url='https://example.com/index.html')
    data = CreateATask_fromUrl(req=req, opt=opt)
    task = self.client.create_a_task_from_url(data=data)
    assert task.code == 0
    # delete task
    while True:
      time.sleep(2)
      task_info = self.client.get_task_info(rid=task.data)
      if (task_info.data.status == TASK_STATUS.DONE):
        break
    delete_response = self.client.delete_a_task(rid=task.data, force=True)
    assert delete_response.code == 0
```

## Create a batch of tasks, get task information.

```python

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
```

## Pause/Continue  one/every Task

```python
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

```