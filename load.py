import os
import yaml




def load_params():
    with open(get_config_file()) as stream:
        data = yaml.safe_load(stream.read())    # load the yaml file
    return data


def get_config_file():
    config_file = './data/simple_data.yaml'
    
    # If the workspace variable is defined, use the config from there, else use default
    if 'IT_WORKSPACE' in os.environ:
        workspace = os.environ['IT_WORKSPACE']
        config_file = workspace + os.environ.get('IT_CONFIG_FILE', '/data/e2e.yaml')
    return config_file


from yaml import load

parameters = dict(
    load_params()["parameters"],
    telemetry=None,
   # EDM_folders=EDM_folders,
)
