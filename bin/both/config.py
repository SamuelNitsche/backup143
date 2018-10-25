import os
from configparser import ConfigParser

def config_var(section, name):
    config = ConfigParser()
    script_dir = os.path.dirname(__file__)
    rel_path = "../../config.ini"
    config_path = os.path.join(script_dir, rel_path)
    if os.path.isfile(config_path) != True:
        file = open(config_path,'w+')
        file.close()
    config.read(config_path)
    try:
        value = config[section][name]
    except KeyError:
        value = False
    return value
	


''' Werte Laden mit config["section"]["varname"] '''