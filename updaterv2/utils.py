__author__ = 'mFoxRU'

import hashlib
from time import strftime

log_file = 'log.log'


def check_hash(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
        buf = afile.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(65536)
    return hasher.hexdigest()


def _log(*args):
    with open(log_file, 'a') as logfile:
        logfile.write(''.join((strftime('[%Y.%m.%d|%H:%M:%S] '),
                               ' '.join(str(x) for x in args), '\n')))