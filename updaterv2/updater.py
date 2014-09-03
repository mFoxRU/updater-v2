__author__ = 'mFoxRU'

import ConfigParser
import urllib2
import json


def load_config(config_file='config.ini'):
    config = ConfigParser.ConfigParser()
    try:
        config.readfp(open(config_file))
    except Exception as e:
        exit('Error loading config file "%s"; %s' % (config_file, e))
    else:
        options = dict(config.items('Main'))
        return options


def get_file_list(update_serv):
    try:
        resp = urllib2.urlopen(update_serv)
    except Exception as e:
        raise e
    else:
        data = json.load(resp)
        return data


def main():
    options = load_config()
    files = get_file_list(options['update_serv'])


if __name__ == '__main__':
    main()