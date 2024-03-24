from aiohttp import web as aiohttp_web, test_utils as aiohttp_test

from app import types as app_types


async def hello(req: aiohttp_web.Request):
    if req.can_read_body:
        body = await req.json()
    else:
        raise aiohttp_web.HTTPException()

    print(body)
    return aiohttp_web.json_response(body)


async def handler(event: app_types.YFunctionEvent, _):
    server = aiohttp_web.Application()
    server.router.add_post('/api/endpoint', hello)

    async with aiohttp_test.TestClient(aiohttp_test.TestServer(server)) as dispatcher:
        async with dispatcher.request(
            event['httpMethod'],
            event['path'],
            params=event['multiValueQueryStringParameters'],
            data=event['body'],
            headers=event['headers']
        ) as resp:
            print(await resp.json())
