import sys
import shlex
import argparse
import dataclasses
import os
import json


@dataclasses.dataclass
class MessageParams:
    sender: str = ''
    recipient: str = ''
    message: str = ''

    @property
    def json_str(self) -> str:
        return json.dumps(self.__dict__)


class CmdParams:
    default_config_file_name = 'config.toml'

    def __init__(self, args_str: str = ''):
        self.message_params_collection: list[MessageParams] = []
        self.config_file: str = self.default_config_file_name
        self._used_files: set[str] = set()

        self._parse_args_row(args_str)

    def _load_from_file(self, file_name: str = '') -> None:
        file_name = os.path.abspath(file_name)
        if file_name and os.path.exists(file_name) and (file_name not in self._used_files):
            self._used_files.add(file_name)

            with open(file_name, mode='r', encoding='utf8') as file:
                lines = file.readlines()
                for line in lines:
                    row = line.strip()
                    if not row.startswith('#'):
                        self._parse_args_row(row)

    def _parse_args_row(self, args_str: str = '') -> None:
        if args_str:
            arg_list = shlex.split(args_str)
        else:
            arg_list = sys.argv[1:]

        if not arg_list:
            return

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('txt', nargs='*', default=[])
        arg_parser.add_argument('-s', '--sender', type=str, default='')
        arg_parser.add_argument('-r', '--recipient', type=str, default='')
        arg_parser.add_argument('-m', '--message', type=str, default='')
        arg_parser.add_argument('-f', '--file', type=str, default='')
        arg_parser.add_argument('-c', '--config', type=str, default='')

        args = arg_parser.parse_args(arg_list)

        if args.config and self.config_file == self.default_config_file_name:
            self.config_file = args.config

        if args.file or args.sender or args.recipient or args.message:
            if args.file:
                self._load_from_file(args.file)

            if args.sender or args.recipient or args.message:
                self.message_params_collection.append(MessageParams(args.sender, args.recipient, args.message))
        else:
            txt_args = [_ for _ in args.txt]

            if txt_args:
                while len(txt_args) < 3:
                    txt_args.append('')

                self.message_params_collection.append(MessageParams(*txt_args[:3]))

