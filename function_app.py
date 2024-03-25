import base64
import json

from aiohttp import web as aiohttp_web, test_utils as aiohttp_test

from app import types as app_types


async def hello(req: aiohttp_web.Request):
    if req.can_read_body:
        body = await req.json()
    else:
        raise aiohttp_web.HTTPException()

    return aiohttp_web.json_response(body)


async def get_hello(req: aiohttp_web.Request):
    return aiohttp_web.json_response({"params": req.query, "path": req.path})


async def handler(event: app_types.YFunctionEvent, ctx):
    print(event)
    print(ctx)

    server = aiohttp_web.Application()
    server.router.add_post('/api/endpoint', hello)
    server.router.add_get('/api/endpoint', get_hello)

    async with aiohttp_test.TestClient(aiohttp_test.TestServer(server)) as dispatcher:
        async with dispatcher.request(
            event['httpMethod'],
            event['url'],
            params=event['multiValueQueryStringParameters'],
            data=(base64.b64decode(event['body']) if event['isBase64Encoded'] else event['body']),
            headers=event['headers'],
        ) as resp:
            y_responst = {
                "statusCode": resp.status,
                "isBase64Encoded": False,
            }

            if resp.status >= 400:
                return y_responst

            y_responst["headers"] = {'Content-Type': 'application/json'},

            body = await resp.json()
            if body is not None:
                y_responst['body'] = json.dumps(body)

            return y_responst
