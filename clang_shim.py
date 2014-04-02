#!/usr/bin/python

__author__ = 'schwa'

import sys
import subprocess
import os
import utilities.jsond as jsond
import traceback
import json

journal_path = 'clang_shim.json'
log_path = 'clang_shim.log'

######################################################################################

import logging
import logging.handlers
logging.basicConfig(
    format='%(process)d:%(levelname)s:%(message)s',
#    filename=log_path,
    level=logging.DEBUG)
logger = logging

#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
#handler = logging.handlers.SysLogHandler() #facility=logging.SysLogHandler.LOG_DAEMON)
#handler.setLevel(logging.DEBUG)
##formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
##fh.setFormatter(formatter)
#logger.addHandler(handler)

######################################################################################

def cc():
    #logger.info('#' * 80)
    #logger.info('SHIM')
    args = ['clang'] + sys.argv[1:]
    #logger.info(' '.join(args))
    #logger.info('#' * 80)

    theResult = subprocess.call(args, shell=False)

    try:
        client = jsond.JSONClient()
        client.write({'args': args})
    except:
        logger.error('{}\n'.format(traceback.format_exc()))

    sys.exit(theResult)


def shim():
    #logger.info('>' * 80)
    #logger.info('BUILD')

    server = jsond.JSONServer()
    server.serve()

    env = server.environ
    env['CC'] = os.path.normpath(os.path.join(os.getcwd(), sys.argv[0]))
    env['CLANG_SHIM'] = '1'

    theResult = subprocess.call(sys.argv[1:], env = env)
    #logger.info('<' * 80)

    data = server.close()
    json.dump(data, open(journal_path, 'w'), sort_keys=True, indent=4, separators=(',', ': '))

    sys.exit(theResult)

if __name__ == '__main__':
    #logger.info(' '.join(sys.argv))

    if 'CLANG_SHIM' not in os.environ:
        shim()
    else:
        cc()
