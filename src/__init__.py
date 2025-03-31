import src.http_client
import src.http_socket_client
import src.http_async_client
import logging

logging.basicConfig(level=logging.INFO,
                    filename='client.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

