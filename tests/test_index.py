from gospeed_api.index import GospeedClient
from gospeed_api.models.post_resolve_a_request import ResolveRequest
from gospeed_api.models import TASK_STATUS

class TestClassGospeedClientInstance:
  client = GospeedClient('http://127.0.0.1:9999/')

  def test_get_server_info(self):
    res = self.client.get_server_info()
    print(str(res))

  def test_resolve_a_request(self):
    req_data = ResolveRequest(url="https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/2c6475e1-e2c5-49e4-8c55-edcb95f4a98d/width=1024/2c6475e1-e2c5-49e4-8c55-edcb95f4a98d.jpeg")
    res = self.client.resolve_a_request(data=req_data)
    #assert res.data.res.files[0].name == '2c6475e1-e2c5-49e4-8c55-edcb95f4a98d.jpeg'
    print(str(res))
  
  def test_get_task_list(self):
    data = self.client.get_task_list({TASK_STATUS.DONE})
    assert data.code == 0
