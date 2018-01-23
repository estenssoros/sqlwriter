import os

import yaml

this_dir = os.path.dirname(__file__)


def get_config(prog=None):
    cfg_file = os.path.join(this_dir, 'conf.yaml')

    with open(cfg_file, 'r') as f:
        config = yaml.load(f)

    if prog is None:
        return config

    try:
        return config[prog]
    except KeyError:
        print('No config found for {}. Exiting now.'.format(prog))
        sys.exit(1)
