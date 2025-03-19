Whatever happens inside Gopeed, every response JSON data that returned from the Gopeed REST API follow same structure for root layer:

- code *{int}*
- msg *{str}*
- data *{Dict | null}*

If code == 0, then data will contain corresponding content, else nothing.

Since this program need to validate every response from Gopeed, we could write a simple validate logic inside data model(pydantic BaseModel) and a throw Error function contain it's code and msg for display.

which implementation were inspired from arktype.

is_success(): bool
throw():
summary(): str // human readable error information.