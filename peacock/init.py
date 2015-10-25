import configparser
import logging


def initialize(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    log_config = config['log']
    level = logging.DEBUG if log_config['debug'] else logging.INFO
    logging.basicConfig(
        filename=log_config['filename'],
        level=level
    )

    return config
