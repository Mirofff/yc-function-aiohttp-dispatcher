import typing as t


class YFunctionEvent(t.TypedDict):
    httpMethod: t.Literal['POST', 'GET', 'HEAD', 'OPTION', 'DELETE', 'PUT', 'PATCH']
    headers: dict
    url: str
    multiValueHeaders: dict
    queryStringParameters: dict
    multiValueQueryStringParameters: dict
    requestContext: dict
    body: str | bytes
    isBase64Encoded: bool


class YFunctionResponse(t.TypedDict):
    statusCode: int
    headers: dict
    isBase64Encoded: bool
    body: str | bytes | None
