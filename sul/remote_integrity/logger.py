#!/usr/bin/env python

from datetime import datetime
from smtplib import SMTP
from email.mime.text import MIMEText

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Logger:

    def __init__(self, config):
 
        self.config = config

    def dispatch_telegram_msg(self, events):

        if not any(events):
            return print("Tidak ada event, skip notifikasi telegram.")

        if not self.config.telegram_api_token:
            return print("Telegram API kosong, tidak akan push ke bot telegram.")

        if not self.config.telegram_api_chat_id:
            return print("Telegram chat id kosong, tidak akan push ke bot telegram.")

        bot = Updater(token=self.config.telegram_api_token).bot
        bot.sendMessage(chat_id=self.config.telegram_api_chat_id, text=self._get_email_body_from_events(events))

    def _get_email_body_from_events(self, events):

        email  = "Halo Admin,\n"
        email += "\n"
        email += "Kami menemukan beberapa perubahan pada:\n"
        email += "\n"
        email += "Server: {name} ({ip}:{port})\n".format(name=self.config.server_name, ip=self.config.server_address, port=self.config.server_port)
        email += "Timestamp: {timestamp}\n".format(timestamp=datetime.now().strftime("%B %d, %Y on %H:%M:%S"))
        email += "Jumlah Incident: {incidents}\n".format(incidents=len(events))
        email += "\n"
        email += "{incidents}\n".format(incidents=self._get_email_body_text_formatted(events))
        email += "\n"
        email += "Untuk keamanan server anda, segera lakukan check pada server."
        return email

    def _get_email_body_text_formatted(self, events):
 
        return "\n".join([e.description for e in events])
