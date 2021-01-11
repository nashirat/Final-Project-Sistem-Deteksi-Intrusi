#!/usr/bin/env python

from axel import Event as EventHandler

from sul.remote_integrity.models import database_exists, create_database, DATABASE_PATH, Server, Checksum, Event


class Integrity:

    def __init__(self, config):
       
        self.config = config
        self.server = None
        self.server_is_new = False
        self.events = []

        self.on_events_detected = EventHandler()

    def load_database(self):
       
        if not database_exists():
            print("[+] Tidak ada database, membuat database baru '{}'".format(DATABASE_PATH))
            create_database()

        if self._server_exists():
            self._load_server()
        else:
            print("[+] Pertama di server '{}', membuat tracker.".format(self.config.server_name))
            print("[?] Note: Perubahan belum bisa terdeteksi karena pertama kali run di server")
            self._add_server()

    def _server_exists(self):
    
        return Server.exists(name=self.config.server_name)

    def _add_server(self):
      
        self.server = Server.create(name=self.config.server_name)
        self.server_is_new = True

    def _load_server(self):
      
        self.server = Server.get(name=self.config.server_name)

    def identify(self, output):
      
        for index, (path, checksum) in enumerate(output):

            checksum_record = self.server.get_related_checksum(path, checksum)

            if checksum_record is None:
                checksum_record = Checksum.create(path=path, checksum=checksum, server=self.server)
                self._handle_file_added(checksum_record)
                continue

            if checksum_record.checksum != checksum:
                self._handle_file_modified(checksum_record, checksum)
                checksum_record.checksum = checksum
                continue

        for checksum_record in self.server.checksums:
            if not any([o for o in output if o[0] == checksum_record.path]):
                self._handle_file_removed(checksum_record)
                checksum_record.delete()

        if any(self.events):
            self.on_events_detected.fire(self._get_events_as_anonymous_obj_list())

    def _get_events_as_anonymous_obj_list(self):

        return [e.to_anonymous_object() for e in self.events]

    def _handle_file_added(self, checksum_record):

        if not self.server_is_new:
            description = "File baru/modifikasi terdeteksi pada '{path}'".format(path=checksum_record.path)
            event = Event.create(event=Event.FILE_ADDED, description=description, checksum=checksum_record)
            self.events.append(event)

    def _handle_file_modified(self, checksum_record, checksum):

        description = "File termodifikasi terdeteksi pada '{path}'".format(path=checksum_record.path)
        event = Event.create(event=Event.FILE_MODIFIED, description=description, checksum=checksum_record)
        self.events.append(event)

    def _handle_file_removed(self, checksum_record):

        description = "File terhapus terdeteksi pada '{path}'".format(path=checksum_record.path)
        event = Event.create(event=Event.FILE_REMOVED, description=description, checksum=checksum_record)
        self.events.append(event)

    def print_statistics(self):

        print("Stats")
        print("File baru/diubah:  {}".format(self._get_addition_event_count()))
        print("File dihapus:  {}".format(self._get_removal_event_count()))

    def _get_addition_event_count(self):

        return len([e for e in self.events if e.event == Event.FILE_ADDED])

    def _get_removal_event_count(self):

        return len([e for e in self.events if e.event == Event.FILE_REMOVED])

    def _get_modified_event_count(self):

        return len([e for e in self.events if e.event == Event.FILE_MODIFIED])