from configparser import ConfigParser
import os

def read_config(section,option):
    current_dir = os.getcwd()
    path = os.path.join(os.path.dirname(current_dir),'etc','pbotinterface.ini')
    config = ConfigParser()
    config.read(path)
    value = config.get(section,option)
    return value