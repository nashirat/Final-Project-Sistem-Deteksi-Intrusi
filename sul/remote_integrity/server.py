#!/usr/bin/env python

import shlex

from paramiko import AutoAddPolicy
from paramiko import RSAKey
from paramiko import SSHClient
from paramiko.ssh_exception import NoValidConnectionsError

from sul.remote_integrity.exceptions import ServerException, DirectoryNotFoundException


class Server:

    def __init__(self, config):

        self.config = config
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.connection = None

    def connect(self):

        try:
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(
                hostname=self.config.server_address,
                port=self.config.server_port,
                username=self.config.auth_username,
                pkey=RSAKey.from_private_key_file(self.config.auth_private_key))

        except NoValidConnectionsError as e:
            raise ServerException(str(e))

    def acquire_checksum_generator(self, path=None):

        for line in self._exec_checksum_list_cmd(path).splitlines():
            try:
                checksum, path = line.split("  ")[0:2]
            except ValueError:
                print("Warning: Tidak bisa melakukan pharsing checksum output '{}'".format(line))
                continue

            if not self._path_is_blacklisted(path):
                yield path, checksum

    def acquire_checksum_list(self):

        output  = list(self.acquire_checksum_generator())

        if self.config.scan_php_modules:
            try:
                path = self._exec_php_extension_dir()
                output += list(self.acquire_checksum_generator(path))
            except DirectoryNotFoundException as e:
                print("{}".format(e))
                print("Install 'php-dev' atau setting path ke php-dev.")

        return output

    def _path_is_blacklisted(self, path):
    
        for directory in self.config.ignore_directories:
            if directory + ("/" if not directory.endswith("/") else "") in path:
                return True

        for file_name in self.config.ignore_files:
            if path.split("/")[-1] == file_name:
                return True

    def _exec_pwd(self):
  
        stdin, stdout, stderr = self.client.exec_command("pwd")
        return stdout.read().decode("utf-8").strip()

    def _exec_home_dir(self):
      
        stdin, stdout, stderr = self.client.exec_command("echo $HOME")
        return stdout.read().decode("utf-8").strip()

    def _exec_checksum_list_cmd(self, path=None):
     
        path = self._get_absolute_start_directory(path)
        command = 'find %s -type f -exec sha512sum "{}" +' % shlex.quote(path)
        stdin, stdout, stderr = self.client.exec_command(command)

        stdout = stdout.read()
        stderr = stderr.read()

        if self._exec_successful(stderr):
            return stdout.decode("utf-8")
        else:
            raise ServerException("Gagal mendapatkan list checksum: {}".format(stderr.decode("utf-8")))

    def _exec_successful(self, stderr):

        return not any(stderr)

    def _exec_php_extension_dir(self):

        stdin, stdout, stderr = self.client.exec_command("php-config --extension-dir")

        if self._exec_successful(stderr):
            return stdout.read().decode("utf-8").strip()
        else:
            raise DirectoryNotFoundException("Direktori PHP gagal didapatkan, skipping..")

    def _get_absolute_start_directory(self, path=None):

        path = path or self.config.start_directory

        if path.startswith("~"):
            path = path.replace("~", self._exec_home_dir())

        if path.startswith("./"):
            path = path.replace("./", self._exec_pwd())

        if not path.startswith("/"):
            path = self._exec_pwd() + "/" + path

        return path
