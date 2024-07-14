# gospeed_api

This project provide Gospeed downloader RestAPI full-covered interacting.

All  data model is type checked in runtime by using [Pydantic](https://docs.pydantic.dev/).

**🎉Async implementation is added in 2.0.0 Version, support both asyncio and [trio](https://github.com/python-trio/trio)!🎉**.

Please use the latest version (for now it's 2.0.4).

Because in 2.0.2 there is a bug which handle url query parameter incorrectly, cause invoking delete endpoint to delete task and file failure!

And It's already resolved in the newest version! ☝️🤓

## install

pypi repo: https://pypi.org/project/gospeed_api/

```powershell
pip install gospeed_api
```

## Usage Example

Every usage example is written in test file, for more detail please take a look: [test_index.py](./tests/test_index.py)

