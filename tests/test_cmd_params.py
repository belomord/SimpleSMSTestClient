import os

import pytest
import src.cmd_params


@pytest.fixture(scope='module')
def prepare_params() -> tuple[str, list[src.cmd_params.MessageParams]]:
    param_file_name1 = "p1.txt"
    param_file_name2 = "p2.txt"
    param_file_name3 = "p3.txt"

    r10 = src.cmd_params.MessageParams('00', '12-34-56', 'This is_a_message.')

    r11 = src.cmd_params.MessageParams('11', '22', 'Message 12')
    r12 = src.cmd_params.MessageParams('33', '44', 'Message 34')
    r13 = src.cmd_params.MessageParams('55', '66', 'Message 56')

    r21 = src.cmd_params.MessageParams('77', '88', "Message 78")

    params_list = [f'-s {r11.sender} -r {r11.recipient} -m "{r11.message}" -c "1.toml"',
                   f'--sender {r12.sender} --recipient {r12.recipient} --message "{r12.message}"',
                   f'{r13.sender} {r13.recipient} "{r13.message}" -c "2.toml"',
                   f'-f {param_file_name1}',
                   f'-f {param_file_name2}']

    with open(param_file_name1, "w") as file:
        file.write('\n'.join(params_list))

    params_list = [f'-s {r21.sender} -r {r21.recipient} -m "{r21.message}"',
                   f'-f {param_file_name3}']

    with open(param_file_name2, "w") as file:
        file.write('\n'.join(params_list))

    print('Test data prepared!')

    yield f'-s {r10.sender} -r {r10.recipient} -m "{r10.message}" -f "{param_file_name1}"', \
        [r11, r12, r13, r21, r10]

    os.remove(param_file_name1)
    os.remove(param_file_name2)
    print('Prepare finished!')


def test_empty_param() -> None:
    _cmd_params = src.cmd_params.CmdParams()
    assert _cmd_params.message_params_collection == []
    assert _cmd_params.config_file == 'config.toml'


def test_params_collection(prepare_params) -> None:
    _cmd_params = src.cmd_params.CmdParams(prepare_params[0])

    assert _cmd_params.message_params_collection == prepare_params[1]
    assert _cmd_params.config_file == '1.toml'


def test_config_params():
    _cmd_params = src.cmd_params.CmdParams('-c "tmp.toml"')

    assert _cmd_params.message_params_collection == []
    assert _cmd_params.config_file == 'tmp.toml'
    