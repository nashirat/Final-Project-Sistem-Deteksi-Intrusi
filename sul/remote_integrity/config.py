#!/usr/bin/env python

import os
from configparser import ConfigParser, NoSectionError, NoOptionError

from sul.remote_integrity.exceptions import ConfigurationException


class Config:

    def __int__(self):

        # [server]
        self.server_name = None
        self.server_port = None
        self.server_address = None

        # [auth]
        self.auth_username = None
        self.auth_private_key = None

        # [filter]
        self.start_directory = None
        self.ignore_files = []
        self.ignore_directories = []
        self.scan_php_modules = True

        # [telegram]
        self.telegram_api_token = None
        self.telegram_api_chat_id = None

    @staticmethod
    def load(path):
        
        if not os.path.exists(path):
            raise ConfigurationException("File config '{}' tidak ada, apakah path sudah benar?".format(path))

        config = Config()
        parser = ConfigParser()
        parser.read(path)

        try:
            config.server_name = parser.get("server", "server_name")
            config.server_port = parser.getint("server", "server_port", fallback=21)
            config.server_address = parser.get("server", "server_address")

            config.auth_username = parser.get("auth", "auth_username")
            config.auth_private_key = os.path.expanduser(parser.get("auth", "auth_private_key"))

            config.ignore_files = parser.get("filter", "ignore_files").split(",") or []
            config.ignore_directories = parser.get("filter", "ignore_directories").split(",") or []
            config.start_directory = parser.get("filter", "start_directory")
            config.scan_php_modules = parser.getboolean("filter", "scan_php_modules")

            config.telegram_api_token = parser.get("telegram", "telegram_api_token") or None

            try:
                config.telegram_api_chat_id = parser.getint("telegram", "telegram_api_chat_id") or None
            except ValueError:
                config.telegram_api_chat_id = None

        except (NoSectionError, NoOptionError) as e:
            raise ConfigurationException("{} di file config '{}'".format(str(e), path))

        for attr in config.__dict__.keys():
            if getattr(config, attr) == "":
                raise ConfigurationException("Missing attribute value '{}' di file config '{}'".format(attr, path))

        return config

