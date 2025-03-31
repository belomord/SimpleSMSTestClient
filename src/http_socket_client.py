import queue
import socket
import threading
import logging

import src.http_mess
import src.cmd_params
import src.file_config
import src.http_url

from src.http_client import HttpClient, RequestResult, HttpClassClientEnum


class HttpSocketClient(HttpClient):
    def _send_single_request(self,
                             request: src.http_mess.HttpRequest,
                             sem: threading.Semaphore,
                             result_queue: queue.Queue,
                             lock: threading.Lock) -> None:

        try:
            with sem:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    if self.server.max_time > 0:
                        sock.settimeout(self.server.max_time / 1000)

                    with lock:
                        logging.info(f'Try to send data by socket: {request.body}')

                    sock.connect((self.url.host, self.url.port))
                    sock.sendall(request.to_bytes())

                    response_data = b''
                    while True:
                        response_part = sock.recv(8192)
                        if not response_part:
                            break
                        response_data += response_part

                    with lock:
                        logging.info(f'Received data:\n{response_data.decode("utf-8")}\n\nFor {request.body}\n' +
                                     '-' * 80 + '\n')

                    result_queue.put(RequestResult(request, src.http_mess.HttpResponse.from_bytes(response_data)))
        except socket.timeout:
            with lock:
                logging.error(f'Socket timeout for {request.body}')

            result_queue.put(RequestResult(request, src.http_mess.HttpResponse(504, 'Socket timeout')))
        except Exception as e:
            with lock:
                logging.error(f'Socket error: {str(e)} for {request.body}')

            result_queue.put(RequestResult(request, src.http_mess.HttpResponse(500, f'Socket error: {str(e)}')))

    def send(self, messages: src.cmd_params.MessageParams | list[src.cmd_params.MessageParams]) -> list[RequestResult]:
        if isinstance(messages, src.cmd_params.MessageParams):
            messages = [messages]

        max_connections = len(messages) if self.server.max_connections <= 0 else self.server.max_connections
        sem = threading.Semaphore(max_connections)
        result_queue: queue.Queue = queue.Queue()
        lock = threading.Lock()
        threads: list[threading.Thread] = []

        for message in messages:
            request = src.http_mess.HttpRequest(url=self.url, user=self.user, body=message.json_str)

            thread = threading.Thread(
                target=self._send_single_request,
                args=(request, sem, result_queue, lock))

            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        results = []

        while not result_queue.empty():
            results.append(result_queue.get())

        return results


HttpSocketClient.register(HttpClassClientEnum.SOCKET)
