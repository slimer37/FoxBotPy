import configparser

def write_default():
    config = configparser.ConfigParser()
    config['User'] = { 'TargetChannel': '--Some username--' }
    config['Client'] = { 'ID': '--The app ID--', 'Secret': 'The app secret' }
    
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def read_config():
    config = configparser.ConfigParser()
    
    if len(config.read('config.ini')) == 0:
        write_default()
        print("No config file was found. An empty one has been created.")
        return None
    
    return config