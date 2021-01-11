#!/usr/bin/env python

from tabulate import tabulate

from sul.remote_integrity.models import Server, Checksum, Event


class Inspector:

    def __init__(self, args):
        self.args = args

    def run(self):

        if self.args.list == "servers":
            return self._list_servers()

        if self.args.list == "checksums":
            return self._list_checksums()

        if self.args.list == "events":
            return self._list_events()

    def _list_servers(self):

        data = Server.query().all()
        print(tabulate([d.values() for d in data], Server.keys(), "grid"))

    def _list_checksums(self):

        data = Checksum.query().all()
        print(tabulate([d.values() for d in data], Checksum.keys(), "grid"))

    def _list_events(self):

        data = Event.query().all()
        print(tabulate([d.values() for d in data], Event.keys(), "grid"))
