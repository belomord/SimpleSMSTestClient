import os
import tomllib
import dataclasses
from abc import ABC, abstractmethod


@dataclasses.dataclass
class User:
    login: str = ""
    password: str = ""


@dataclasses.dataclass
class Server:
    address: str = ""
    max_connections: int = 0
    max_time: int = 0


@dataclasses.dataclass
class System:
    client_type: int = 0


class FileConfig(ABC):
    def __init__(self, file_name: str = 'config.toml'):
        self.user = User()
        self.server = Server()
        self.system = System()

        self._load_from_file(file_name)

    @abstractmethod
    def _load_from_file(self, file_name: str) -> None:
        ...


class TomlConfig(FileConfig):
    def _load_from_dict(self, cfg: dict) -> None:
        self.user = User(login=cfg.get('user', {}).get('login', ''),
                         password=cfg.get('user', {}).get('password', ''))

        self.server = Server(address=cfg.get('server', {}).get('address', ''))
        self.system = System(client_type=cfg.get('system', {}).get('client_type', 0))

    def _load_from_file(self, file_name: str) -> None:
        cfg = dict()

        if file_name.strip() and os.path.exists(file_name):
            with open(file_name, "rb") as file:
                cfg = tomllib.load(file)

        self._load_from_dict(cfg)
