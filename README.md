# Go~~s~~peed_api

![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

This project provide [Go~~s~~peed downloader](https://gopeed.com/) RestAPI full-covered interacting.

> Sorry about that I made a mistake about its name. I realized that when I finished version 2.0.4;
> 🎶~~It's too Laaaaate~ to Apologiiiiiize~, It's too Laaaaaaaaaaaate~~🎶

Every function's input and output will get type checking in runtime by using [Pydantic](https://docs.pydantic.dev/).

**🎉Async implementation is added in 2.0.0 Version, support both asyncio and [trio](https://github.com/python-trio/trio)!🎉**.

Please use the latest version.

Because in 2.0.2 there is a bug which handle url query parameter incorrectly, cause invoking delete endpoint to delete task and file failure!

And It's already resolved in the newest version! ☝️🤓

## install

gospeed-api package [address](https://pypi.org/project/gospeed-api/).

```powershell
pip install gospeed-api
```

## Usage Example

Every usage example is written in test file, for more detail please take a look: [test_index.py](./tests/test_index.py)

## The future improvements were on plan

2025/1/6/

1. After a few months at the end of development, I'm supposed to rewrite the usage guide. Because recently, when I was trying to write some script based on this library, I could feel there was not enough introduction to make things clear for the user.
2. Update to version 3.0.0. This major update will create a new implementation with a more intuitive usage experience.

I'm starting achiving these two objectives from the day I wrote above.

---

2025/2/22/

Now AsyncGospeedClient have an optional init paramter "httpx_async_client" to receive customized async httpx client object to send requests.

---

2025/3/20

Now Ver3.0 dev finished!
With 100% test coverage, simplified function usage and usage example. See [test_index.py](./tests/test_index.py).
