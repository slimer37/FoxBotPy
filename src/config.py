import configparser


def write_default() -> None:
    config = configparser.ConfigParser()
    config['User'] = {}
    config['User']['TargetChannel'] = 'Some username'
    config['User']['PunChancePercentage'] = '50'
    config['Client'] = {}
    config['Client']['ID'] = 'The app ID'
    config['Client']['Secret'] = 'The app secret'

    with open('config.ini', 'w') as config_file:
        config.write(config_file)


def read_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()

    if len(config.read('config.ini')) == 0:
        write_default()
        print("No config file was found. An empty one has been created.")
        return None

    return config
