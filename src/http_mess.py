from abc import ABC, abstractmethod
import base64
from typing import Tuple

import src.http_url
import src.file_config


class HttpMessage(ABC):
    @abstractmethod
    def to_bytes(self) -> bytes:
        ...

    @classmethod
    @abstractmethod
    def from_bytes(cls, binary_data: bytes) -> 'HttpMessage':
        ...

    @staticmethod
    def parse_http_message(message: bytes | str) -> Tuple[list[str], dict, str]:
        header = []
        body = ''
        params = dict()

        if isinstance(message, bytes):
            message = message.decode()

        lst = message.split('\r\n\r\n')
        if len(lst) >= 2:
            body = lst[1].strip()

        if lst:
            lst = lst[0].split('\r\n')
            if lst:
                header = lst[0].split()
                for param_str in lst[1:]:
                    if ':' not in param_str:
                        continue

                    param = param_str.split(':', 1)
                    params[param[0].strip()] = param[1].strip()

        return header, params, body


class HttpRequest(HttpMessage):
    def __init__(self, url: src.http_url.HttpUrl, user: src.file_config.User, body: str = ''):
        self.url = url
        self.user = user
        self.body = body

    def to_bytes(self) -> bytes:
        authorization = f"{self.user.login}:{self.user.password}"
        authorization = base64.b64encode(authorization.encode()).decode()

        request_str = (
            f'POST {self.url.path} HTTP/1.1\r\n'
            f'Host: {self.url.host}:{self.url.port}\r\n'
            f'Authorization: Basic {authorization}\r\n'
            'Connection: close\r\n'
        )

        if self.body:
            request_str += f'Content-Type: application/json\r\n'
            request_str += f'Content-Length: {len(self.body)}\r\n\r\n'
            request_str += f'{self.body}'

        return request_str.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> 'HttpRequest':
        header, params, body = cls.parse_http_message(binary_data)

        while len(header) < 2:
            header.append('')

        path = header[1].split('?', 1)[0]
        host = params.get('Host', '')

        if ':' in host:
            host, port = host.split(':', 1)
            port = int(port)
        else:
            port = params.get('Port', 0)

        authorization = params['Authorization']
        if authorization.startswith('Basic '):
            authorization = authorization[6:]
            authorization = base64.b64decode(authorization).decode()
            login, password = authorization.split(':', 1)
            user = src.file_config.User(login, password)
        else:
            user = src.file_config.User()

        url = src.http_url.HttpUrl(protocol='http', host=host, port=port, path=path)
        return HttpRequest(url, user, body)


class HttpResponse(HttpMessage):
    def __init__(self, code: int, message: str, body: str = ''):
        self.code = code
        self.message = message
        self.body = body

    def to_bytes(self) -> bytes:
        response_str = (
            f'HTTP/1.1 {self.code} {self.message}\r\n'
        )

        if self.body:
            response_str += f'Content-Type: application/json\r\n'
            response_str += f'Content-Length: {len(self.body)}\r\n\r\n'
            response_str += f'{self.body}'

        return response_str.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> 'HttpResponse':
        header, params, body = cls.parse_http_message(binary_data)
        code = header[1] if len(header) >= 2 else 0
        message = header[2] if len(header) >= 3 else ''

        return HttpResponse(int(code), message, body)
