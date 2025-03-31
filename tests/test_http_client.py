from typing import Callable

import pytest
import os

import src.cmd_params
from src.cmd_params import CmdParams
from src.http_client import HttpClassClientEnum, RequestResult, HttpClient
from src.http_socket_client import HttpSocketClient
from src.http_async_client import HttpAsyncClient
from src.cmd_params import MessageParams
from src.file_config import TomlConfig, FileConfig

test_params_file = 'tests/test_params.txt'
correct_config_file = 'tests/correct_config.toml'
default_param_str = f'-f {test_params_file} -c {correct_config_file}'


def prepare_params(param_str: str = default_param_str) -> tuple[CmdParams, FileConfig]:
    cmd_params = src.cmd_params.CmdParams(param_str)
    cfg = TomlConfig(cmd_params.config_file)

    return cmd_params, cfg


def test_http_client_fabric():
    assert HttpClient.fabric(HttpClassClientEnum.SOCKET) == HttpSocketClient
    assert HttpClient.fabric(HttpClassClientEnum(0)) == HttpSocketClient
    assert HttpClient.fabric(HttpClassClientEnum.ASYNC) == HttpAsyncClient
    assert HttpClient.fabric(HttpClassClientEnum(1)) == HttpAsyncClient


def test_non_correct_http_client_fabric_param():
    with pytest.raises(NotImplementedError):
        HttpClient.fabric(100)


def _test_http_client(client: HttpClient,
                      messages: list[MessageParams],
                      correct_response_code: int,
                      correct_response_body: str = ''):

    result = client.send(messages)

    assert len(messages) == len(result)

    for r in result:
        assert r.response.code == correct_response_code

        if correct_response_body:
            assert r.response.body == correct_response_body


CorrectionFunction = Callable[[CmdParams, FileConfig], None]


def prepare_client(client_type: HttpClassClientEnum,
                   params_str: str = default_param_str,
                   correct_func: CorrectionFunction | None = None) -> tuple[HttpClient, CmdParams, FileConfig]:
    cmd_params, cfg = prepare_params(params_str)

    if correct_func is not None:
        correct_func(cmd_params, cfg)

    client = HttpClient.fabric(client_type)(server=cfg.server, user=cfg.user)

    return client, cmd_params, cfg


def correct_path(_cmd_params: CmdParams, _cfg: FileConfig):
    _cfg.server.address = _cfg.server.address.replace('/send_sms', '/invalid/path')


def correct_host(_cmd_params: CmdParams, _cfg: FileConfig):
    _cfg.server.address = _cfg.server.address.replace('localhost', 'invalidhost')


def test_socket_client():
    client, cmd_params, cfg = prepare_client(HttpClassClientEnum.SOCKET)
    _test_http_client(client, cmd_params.message_params_collection, 200)


def test_socket_client_body():
    client, cmd_params, cfg = prepare_client(HttpClassClientEnum.SOCKET)
    _test_http_client(client, cmd_params.message_params_collection, 200, '{"status":"success","message_id":"123456"}')


def test_socket_client_invalid_path():
    client, cmd_params, cfg = prepare_client(HttpClassClientEnum.SOCKET, correct_func=correct_path)
    _test_http_client(client, cmd_params.message_params_collection, 404, '')


def test_socket_client_invalid_host():
    client, cmd_params, cfg = prepare_client(HttpClassClientEnum.SOCKET, correct_func=correct_host)
    _test_http_client(client, cmd_params.message_params_collection, 500, '')


def test_async_client():
    client, cmd_params, cfg = prepare_client(HttpClassClientEnum.ASYNC)
    _test_http_client(client, cmd_params.message_params_collection, 200)


def test_async_client_body():
    client, cmd_params, cfg = prepare_client(HttpClassClientEnum.ASYNC)
    _test_http_client(client, cmd_params.message_params_collection, 200, '{"status":"success","message_id":"123456"}')


def test_async_client_invalid_path():
    client, cmd_params, cfg = prepare_client(HttpClassClientEnum.ASYNC, correct_func=correct_path)
    _test_http_client(client, cmd_params.message_params_collection, 404, '')


def test_async_client_invalid_host():
    client, cmd_params, cfg = prepare_client(HttpClassClientEnum.ASYNC, correct_func=correct_host)
    _test_http_client(client, cmd_params.message_params_collection, 500, '')
