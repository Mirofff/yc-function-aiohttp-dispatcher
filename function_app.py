import logging

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
    logging.info(event)
    logging.info(ctx)

    server = aiohttp_web.Application()
    server.router.add_post('/api/endpoint', hello)

    async with aiohttp_test.TestClient(aiohttp_test.TestServer(server)) as dispatcher:
        async with dispatcher.request(
            event['httpMethod'],
            event['url'],
            params=event['multiValueQueryStringParameters'],
            json=event['body'],
            headers=event['headers'],
        ) as resp:
            return {
                "statusCode": 200,
                "headers": {'Content-Type': 'application/json'},
                "multiValueHeaders": {},
                "body": await resp.json(),
                "isBase64Encoded": False,
            }
