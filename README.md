# TP_HTTP_Request_Response_Parser

```
from TP_HTTP_Request_Response_Parser import *

# Parsing HTTP Request
rawRequest = """GET /v1/promo/extension HTTP/2
Host: d2y7f743exec8w.cloudfront.net
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36
Connection: close
Cache-Control: max-age=0


"""

RequestParser = TP_HTTP_REQUEST_PARSER(rawRequest)

print(RequestParser.request_method)
print(RequestParser.request_path)
print(RequestParser.request_query)
print(RequestParser.request_fragment)
print(RequestParser.request_headers.getObject())
print(RequestParser.request_body)



# Parsing HTTP Response
rawResponse = """HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
Server: nginx
Date: Mon, 21 Aug 2023 03:55:08 GMT
Etag: W/"846e0a9b390c273d2d7a6843085411d1"
Cache-Control: max-age=0, private, must-revalidate
X-Request-Id: 06024e22-f233-4517-b0f6-f444c8464e7b
Strict-Transport-Security: max-age=63072000; includeSubDomains
Strict-Transport-Security: max-age=63072000; preload
Vary: Accept-Encoding,Accept
X-Cache: Miss from cloudfront
Via: 1.1 19175f36fb9c16ba394561bae28598da.cloudfront.net (CloudFront)
X-Amz-Cf-Pop: SGN50-P2
X-Amz-Cf-Id: eKssgTNGDCswPiQtSYFD1MRNBJCTHEbnQp4MQjtQx2B4eM7oqXYIHg==

{"ok":true,"promo":[]}
"""

ResponseParser = TP_HTTP_RESPONSE_PARSER(rawResponse)

print(ResponseParser.status_code)
print(ResponseParser.status_text)
print(ResponseParser.response_headers.getObject())
print(ResponseParser.response_body)
```
