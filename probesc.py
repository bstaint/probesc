#!/usr/bin/env python
# coding: utf-8
import argparse

from libs.probesc import ProbeEngine
from libs.utils import runtime, cprint
from libs.exception import *


def get_cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Target URL (e.g. "http://localhost/")')
    parser.add_argument('-m', '--modules', type=lambda s: s.split(','), 
                        help='specific plugin modules.')
    parser.add_argument('-s', '--silent', action='store_true',
                        help='silent execution, don\'t ask.')
    parser.add_argument('-r', '--redirect', action='store_true',
                        help='redirect target hosts ip.')
    return parser.parse_args()

def main(args):
    cprint('starting at %s\n' % runtime(), '*')
    try:
        cprint('testing if the target URL is stable', '*')
        pe = ProbeEngine(args)
        # output target ip
        ip, host = pe.target.ip, pe.target.host
        cprint('%s (%s)' % (ip, host) if ip != host else ip, '+')
        pe.pentest()
    except (TargetError, PluginError), e:
        cprint('%s' % e, '-')
    except KeyboardInterrupt:
        cprint('user quit', '-')
    finally:
        cprint('shutting down at %s' % runtime(), '*', True)

if __name__ == "__main__":
    main(get_cmd_args())
