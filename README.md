# Go~~s~~peed_api

This project provide [Go~~s~~peed downloader](https://gopeed.com/) RestAPI full-covered interacting.

> Sorry about that I made a mistake about its name. I realized that when I finished version 2.0.4;

> 🎶~~It's too Laaaaate~ to Apologiiiiiize~, It's too Laaaaaaaaaaaate~~🎶


All data model is type checked in runtime by using [Pydantic](https://docs.pydantic.dev/).

**🎉Async implementation is added in 2.0.0 Version, support both asyncio and [trio](https://github.com/python-trio/trio)!🎉**.

Please use the latest version (for now it's 2.0.4).

Because in 2.0.2 there is a bug which handle url query parameter incorrectly, cause invoking delete endpoint to delete task and file failure!

And It's already resolved in the newest version! ☝️🤓

## install

pypi repo: https://pypi.org/project/gospeed-api/

```powershell
pip install gospeed-api
```

## Usage Example

Every usage example is written in test file, for more detail please take a look: [test_index.py](./tests/test_index.py)

## The future improvements were on plan

1. I was supposed to use Pydantic from the beginning to help with input validation, but it caused too many unnecessary statements to be written. So the next major update will have some breaking changes.
2. Add error response message check function.
