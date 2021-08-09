'''
    Command line behavior for {{cookiecutter.project_slug}}pkg
'''
from __future__ import print_function

import os
import sys
import argparse
import textwrap
from configparser import ConfigParser

import pyrpkg
from pyrpkg.cli import cliClient
from pyrpkg import rpkgError


class Client(cliClient):
    def __init__(self, config, name='{{cookiecutter.project_slug}}pkg'):
        self.DEFAULT_CLI_NAME = name

        super(Client, self).__init__(config, name)


def run(*args, **kwargs):
        program_name = os.path.basename(sys.argv[0])
        default_user_config_path = os.path.join(
            os.path.expanduser('~'),
            '.config', 'rpkg',
            '%s.conf' % program_name
        )

        parser = pyrpkg.cli.ArgumentParser(add_help=False, allow_abbrev=False)
        parser.add_argument(
            '-C',
            '--config',
            help='Specify a config file to use',
            default='/etc/rpkg/%s.conf' % program_name)
                
        parser.add_argument(
            '--user-config',
            help='Specify a user config file to use',
            default=default_user_config_path)
        (args, other) = parser.parse_known_args()

        if len(other) == 0:
            other = ['-h']

        if not os.path.exists(args.config) and not other[-1] in ['--help', '-h', 'help']:
            sys.stderr.write('Invalid config file %s\n' % args.config)
            sys.exit(1)
        
        config = ConfigParser()
        config.read(args.config)
        config.read(args.user_config)                           
        client = Client(config, name=program_name)                                
        client.do_imports(site='{{cookiecutter.project_slug}}pkg')                                            
        client.parse_cmdline()

        if not client.args.path:            
            try:
                client.args.path = pyrpkg.utils.getcwd()
            except Exception:
                sys.stderr.write('Could not get current path, have you deleted it?\n')
                sys.exit(1)
        
        if client.args.v:            
            log.setLevel(logging.DEBUG)
        elif client.args.q:
            log.setLevel(logging.WARNING)
        else:                                                    
            log.setLevel(logging.INFO)
                
        try:
            sys.exit(client.args.command())
        except KeyboardInterrupt:                                        
            pass
        except Exception as e:                                                   
            if getattr(client.args, 'debug', False):
                raise
            log.error('Could not execute %s: %s' % (client.args.command.__name__, e))
            sys.exit(1)


def main():
    run()
