__author__ = 'mFoxRU'

import os
import ConfigParser
import urllib2
import json

from utils import check_hash


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


def remove_files(folder, file_list):
    files = os.listdir(folder)
    # Had lots of map and filter below, removed for readability
    for afile in files:
        afile_with_path = '\\'.join((folder, afile))
        if not os.path.isfile(afile_with_path):
            continue
        if afile in file_list:
            continue
        try:
            os.remove(afile_with_path)
        except Exception as e:
            exit('Could not remove a file "%s"; %s' % (afile_with_path, e))


def download_file(folder, afile, remote_folder):
    afile_with_path = '\\'.join((folder, afile))
    afile_remote_path = '/'.join((remote_folder, afile))
    try:
        download_afile = urllib2.urlopen(afile_remote_path)
    except Exception as e:
        exit('Error downloading file "%s"; %s' % (afile_remote_path, e))
    else:
        with open(afile_with_path, 'wb') as output:
            output.write(download_afile.read())


def update(folder, files, remote_folder):
    for afile, ahash in files.iteritems():
        afile_with_path = '\\'.join((folder, afile))
        if os.path.isfile(afile_with_path):
            if check_hash(afile_with_path) == ahash.lower():
                continue
            else:
                try:
                    os.remove(afile_with_path)
                except Exception as e:
                    exit('Could not remove a file "%s"; %s' % (afile_with_path,
                                                               e))
        download_file(folder, afile, remote_folder)


def main():
    options = load_config()
    files = get_file_list(options['update_serv'])
    # Remove needless files
    remove_files(options['local_folder'], files.keys())
    update(options['local_folder'], files, options['remote_folder'])

if __name__ == '__main__':
    main()