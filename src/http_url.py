class HttpUrl:
    protocol: str
    port: int
    host: str
    path: str

    def __init__(self, protocol: str = 'http', host: str = '', port: int = 0, path: str = '/') -> None:
        self.protocol = protocol if protocol else 'http'
        self.port = port if port else 80 if protocol == 'http' else 443 if protocol == 'https' else port
        self.host = host if host else 'localhost'
        self.path = path if path else '/'

    def __str__(self) -> str:
        return f'{self.protocol}://{self.host}:{self.port}{self.path}'

    def __repr__(self) -> str:
        return repr(self.__dict__)

    @property
    def address(self) -> str:
        return str(self)

    @classmethod
    def from_address(cls, address: str) -> 'HttpUrl':
        address = address.strip().lower()

        if address.startswith('http://'):
            protocol = 'http'
            address = address[7:]
        elif address.startswith('https://'):
            protocol = 'https'
            address = address[8:]
        else:
            protocol = ''

        host_and_port, *path_parts = address.split('/', 1)
        path = '/' + path_parts[0] if path_parts else '/'

        if ':' in host_and_port:
            host, port_str = host_and_port.split(':')
            port = int(port_str) if port_str.isdigit() else 0
        else:
            host = host_and_port
            port = 80 if protocol == 'http' else 443 if protocol == 'https' else 0

        return cls(protocol, host, port, path)

