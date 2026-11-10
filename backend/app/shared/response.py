from fastapi import Request


def success(request: Request, data: object) -> dict:
    return {'data': data, 'request_id': request.state.request_id}


def failure(request: Request, code: str, message: str, details: object | None = None) -> dict:
    return {
        'error': {'code': code, 'message': message, 'details': details or {}},
        'request_id': request.state.request_id,
    }
