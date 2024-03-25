import base64
import json

from aiohttp import web as aiohttp_web, test_utils as aiohttp_test

from app import types as app_types


async def hello(req: aiohttp_web.Request):
    if req.can_read_body:
        body = await req.json()
    else:
        raise aiohttp_web.HTTPException()

    print(body)
    return aiohttp_web.json_response(body)


async def handler(event: app_types.YFunctionEvent, ctx):
    print(event)
    print(ctx)

    server = aiohttp_web.Application()
    server.router.add_post('/api/endpoint', hello)

    async with aiohttp_test.TestClient(aiohttp_test.TestServer(server)) as dispatcher:
        async with dispatcher.request(
            event['httpMethod'],
            event['url'],
            params=event['multiValueQueryStringParameters'],
            data=(base64.b64decode(event['body']) if event['isBase64Encoded'] else event['body']),
            headers=event['headers'],
        ) as resp:
            return {
                "statusCode": 200,
                "headers": {'Content-Type': 'application/json'},
                "multiValueHeaders": {},
                "body": json.dumps(await resp.json()) if resp.status in (200, 201,) else None,
                "isBase64Encoded": False,
            }
