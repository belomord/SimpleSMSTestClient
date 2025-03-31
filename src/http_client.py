import dataclasses
from abc import ABC, abstractmethod
from enum import IntEnum

import src.http_mess
import src.cmd_params
import src.file_config
import src.http_url


class HttpClassClientEnum(IntEnum):
    SOCKET = 0
    ASYNC = 1


@dataclasses.dataclass
class RequestResult:
    request: src.http_mess.HttpRequest
    response: src.http_mess.HttpResponse


class HttpClient(ABC):
    RegClasses: dict[HttpClassClientEnum, type['HttpClient']] = {}

    def __init__(self, server: src.file_config.Server, user: src.file_config.User):
        self.server = server
        self.user = user
        self.url = src.http_url.HttpUrl.from_address(server.address)

    @abstractmethod
    def send(self, messages: src.cmd_params.MessageParams | list[src.cmd_params.MessageParams]) -> list[RequestResult]:
        ...

    @classmethod
    def register(cls, client_type: HttpClassClientEnum):
        cls.RegClasses[client_type] = cls
        return cls

    @classmethod
    def fabric(cls, client_type: int | HttpClassClientEnum) -> type['HttpClient']:
        try:
            if not isinstance(client_type, HttpClassClientEnum):
                client_type = HttpClassClientEnum(client_type)
            return cls.RegClasses[client_type]
        except ValueError:
            raise NotImplementedError(f'HttpClient class for client_type = {client_type} not registered.')
        except KeyError:
            raise NotImplementedError(f'HttpClient class for client_type = {client_type} not registered.')
        except Exception as e:
            raise e
