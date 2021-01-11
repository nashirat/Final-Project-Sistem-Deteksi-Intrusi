#!/usr/bin/env python
import time
from argparse import ArgumentParser

from sul.remote_integrity.exceptions import SulException
from sul.remote_integrity.config import Config
from sul.remote_integrity.inspector import Inspector
from sul.remote_integrity.logger import Logger
from sul.remote_integrity.server import Server
from sul.remote_integrity.integrity import Integrity
from sul.remote_integrity.models import session as database


def main():

    try:
        args = load_arguments()

        if args.config:
            return dispatch_remote_integrity_checker(args)

        if args.list:
            return dispatch_database_inspector(args)

    except SulException as e:
        print("[!] Error: {}".format(e))


def dispatch_remote_integrity_checker(args):

    config = load_config(path=args.config)

    server = Server(config=config)
    server.connect()
    output  = server.acquire_checksum_list()

    logger = Logger(config=config)
    integrity = Integrity(config=config)

    integrity.on_events_detected += logger.dispatch_telegram_msg

    integrity.load_database()
    integrity.identify(output)
    integrity.print_statistics()

    database.commit()


def dispatch_database_inspector(args):

    inspector = Inspector(args)
    inspector.run()


def load_arguments():

    parser = ArgumentParser(description="DearBytes remote file integrity checker")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--config", help="Path to the server configuration file")
    group.add_argument("-l", "--list", help="List data from the local database")
    return parser.parse_args()


def load_config(path):

    return Config.load(path)


if __name__ == '__main__':
    main()
       
