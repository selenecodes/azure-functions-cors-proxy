import requests
import azure.functions as func
import json

methods = {
    'get': requests.get,
    'delete': requests.delete,
    'post': requests.post,
    'put': requests.put,
    'patch': requests.patch,
    'head': requests.head,
    'options': requests.options
}


def request_from_api(headers, method, data, url):
    if data:
        return methods[method](url, headers=headers, json=data)
    else:
        return methods[method](url, headers=headers)


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()

    if body:
        url = body.get('url', None)
        method = body.get('method', 'get')

        if not url:
            return func.HttpResponse(json.dumps({
                "message": "Please provide a url",
                "code": 400
            }), status_code=400)

        if not method in methods:
            return func.HttpResponse(json.dumps({
                "message": f"Method: {method}, is not supported please use one of: {','.join(list(methods.keys()))}.",
                "code": 405
            }), status_code=405)

        response = request_from_api(
            headers=body.get('headers', None), 
            method=method, 
            data=body.get('data', None), 
            url=url
        )
        
        if not response.ok:
            return func.HttpResponse(json.dumps({
                "message": response.reason,
                "code": response.status_code
            }), status_code=response.status_code)

        response_body = response.json()
        return func.HttpResponse(
            json.dumps(response_body if response_body else {}),
            status_code=200
        )
    
    return func.HttpResponse(json.dumps({ 
        "message": "Please provide a request body!",
        "code": 400
    }), status_code=400)
