import os
import pytest
import src.file_config


@pytest.fixture(scope='module')
def prepare_config():
    file_lines = [
        '[user]',
        'login = "user"',
        'password = "password"',
        '',
        '[server]',
        'address = "http://localhost:4010/send_sms"'
    ]

    file_path = 'test.toml'
    with open(file_path, 'w') as file:
        file.write('\n'.join(file_lines))
    yield file_path
    os.remove(file_path)


def test_empty_cfg():
    cfg = src.file_config.TomlConfig('')
    assert cfg.user.login == ''
    assert cfg.user.password == ''
    assert cfg.server.address == ''


def test_correct_cfg(prepare_config):
    cfg = src.file_config.TomlConfig(prepare_config)
    assert cfg.user.login == 'user'
    assert cfg.user.password == 'password'
    assert cfg.server.address == 'http://localhost:4010/send_sms'
