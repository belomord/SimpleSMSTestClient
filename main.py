import logging

import src.cmd_params
import src.file_config
from src.http_client import HttpClient

logging.info('*********************** Application started ***********************')

cmd_params = src.cmd_params.CmdParams()
cfg = src.file_config.TomlConfig(cmd_params.config_file)
client = HttpClient.fabric(cfg.system.client_type)(server=cfg.server, user=cfg.user)
results = client.send(cmd_params.message_params_collection)

for result in results:
    print(f"code: {result.response.code}; body: '{result.response.body}'")


