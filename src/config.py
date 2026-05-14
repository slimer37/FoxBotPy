from configparser import ConfigParser
import os

config_file_path = "config.ini"

def config_file_exists() -> bool:
    return os.path.exists(config_file_path)

def write_default_config() -> None:
    config = ConfigParser()
    config['User'] = {}
    config['User']['TargetChannel'] = 'Some username'
    config['User']['PunChancePercentage'] = '50'
    config['Client'] = {}
    config['Client']['ID'] = 'The app ID'
    config['Client']['Secret'] = 'The app secret'

    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

def read_config() -> ConfigParser:
    config = ConfigParser()

    if len(config.read(config_file_path)) == 0:
        raise Exception("Couldn't read config file.")

    return config
