import asyncio
import logging

import src.http_mess
import src.cmd_params
import src.file_config
import src.http_url

from src.http_client import HttpClient, RequestResult, HttpClassClientEnum


class HttpAsyncClient(HttpClient):
    def send(self, messages: src.cmd_params.MessageParams | list[src.cmd_params.MessageParams]) -> list[RequestResult]:
        if isinstance(messages, src.cmd_params.MessageParams):
            messages = [messages]

        return asyncio.run(self._async_send(messages))

    async def _async_send(self, messages: list[src.cmd_params.MessageParams]) -> list[RequestResult]:
        max_connections = len(messages) if self.server.max_connections <= 0 else self.server.max_connections
        sem = asyncio.Semaphore(max_connections)

        # Следуем заветам дядюшки Боба. (SRP)
        async def task_sem_wrapper(message: src.cmd_params.MessageParams) -> RequestResult:
            async with sem:
                return await self._send_single_request(message)

        tasks = [task_sem_wrapper(message) for message in messages]
        return await asyncio.gather(*tasks)

    async def _send_single_request(self, message: src.cmd_params.MessageParams) -> RequestResult:
        request = src.http_mess.HttpRequest(
            url=self.url,
            user=self.user,
            body=message.json_str
        )
        writer_stream = None

        try:
            timeout = self.server.max_time / 1000 if self.server.max_time > 0 else None

            logging.info(f'Try to send data by asyncio: {request.body}')
            connection_cor = asyncio.open_connection(self.url.host, self.url.port)
            reader_stream, writer_stream = await asyncio.wait_for(connection_cor, timeout=timeout)

            writer_stream.write(request.to_bytes())
            await asyncio.wait_for(writer_stream.drain(), timeout=timeout)

            response_data = b''
            while True:
                response_part = await asyncio.wait_for(reader_stream.read(8192), timeout=timeout)

                if not response_part:
                    break

                response_data += response_part

            response = src.http_mess.HttpResponse.from_bytes(response_data)
            res = RequestResult(request, response)
            logging.info(f'Received data:\n{response_data.decode("utf-8")}\n\nFor {request.body}\n' + '-' * 80 + '\n')

        except asyncio.TimeoutError:
            logging.error(f'Socket timeout for {request.body}')
            res = RequestResult(request, src.http_mess.HttpResponse(504, "Socket timeout"))
        except Exception as e:
            logging.error(f'Socket error: {str(e)} for {request.body}')
            res = RequestResult(request, src.http_mess.HttpResponse(500, f"Error: {str(e)}"))
        finally:
            if writer_stream:
                writer_stream.close()
                try:
                    await asyncio.wait_for(writer_stream.wait_closed(), timeout=1)
                except:
                    ...

        return res


HttpAsyncClient.register(HttpClassClientEnum.ASYNC)
