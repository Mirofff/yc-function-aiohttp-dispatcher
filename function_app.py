import asyncio
import json
import uuid

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


if __name__ == "__main__":
    y_event = {
        "httpMethod": "POST",
        "headers": {
            "Accept": "*/*",
            "Content-Length": "13",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "curl/7.58.0",
            "X-Real-Remote-Address": "[88.99.0.24]:37310",
            "X-Request-Id": "cd0d12cd-c5f1-4348-9dff-c50a78f1eb79",
            "X-Trace-Id": "92c5ad34-54f7-41df-a368-d4361bf376eb"
        },
        "path": "/api/endpoint",
        "multiValueHeaders": {
            "Accept": ["*/*"],
            "Content-Length": ["13"],
            "Content-Type": ["application/x-www-form-urlencoded"],
            "User-Agent": ["curl/7.58.0"],
            "X-Real-Remote-Address": ["[88.99.0.24]:37310"],
            "X-Request-Id": ["cd0d12cd-c5f1-4348-9dff-c50a78f1eb79"],
            "X-Trace-Id": ["92c5ad34-54f7-41df-a368-d4361bf376eb"]
        },
        "queryStringParameters": {
            "a": "2",
            "b": "1"
        },
        "multiValueQueryStringParameters": {
            "a": ["1", "2"],
            "b": ["1"]
        },
        "requestContext": {
            "identity": {
                "sourceIp": "88.99.0.24",
                "userAgent": "curl/7.58.0"
            },
            "httpMethod": "POST",
            "requestId": "cd0d12cd-c5f1-4348-9dff-c50a78f1eb79",
            "requestTime": "26/Dec/2019:14:22:07 +0000",
            "requestTimeEpoch": 1577370127
        },
        "body": json.dumps({"some": 123}),
        "isBase64Encoded": True,
    }

    y_context = {
        "requestId": str(uuid.uuid4()),
        "functionName": str(uuid.uuid4()),
        "functionVersion": "v0.2.4",
        "memoryLimitInMB": "256Mb",
        "token": None,
    }

    asyncio.run(handler(y_event, y_context))
