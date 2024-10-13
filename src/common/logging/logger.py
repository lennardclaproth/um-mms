import datetime
import os
import logging
import time
from cryptography.fernet import Fernet
from abc import ABC, abstractmethod

from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from common.logging.log import Log


class LoggerInterface(ABC):

    @abstractmethod
    def warning(self, message: str, **kwargs):
        pass

    @abstractmethod
    def info(self, message: str, **kwargs):
        pass

    @abstractmethod
    def error(self, message: str, **kwargs):
        pass

    @abstractmethod
    def suspicious(self, message: str, **kwargs):
        pass


class CustomLogger(LoggerInterface, metaclass=AutoWire):
    def __init__(self, encoder: Encoder):
        self.log_file = "data/logs.txt"
        self.encrypted_log_file = f"{self.log_file}.lcenc"
        self._encoder = encoder
        self.logger = logging.getLogger('FileLogger')
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

        if not os.path.exists(self.log_file):
            open(self.log_file, 'a').close()

    def warning(self, message: str, **kwargs):
        # self.logger.warning(self._format_message(message, **kwargs))
        self._log_to_file('WARNING', message, **kwargs)

    def info(self, message: str, **kwargs):
        # self.logger.info(self._format_message(message, **kwargs))
        self._log_to_file('INFO', message, **kwargs)

    def error(self, message: str, **kwargs):
        # self.logger.error(self._format_message(message, **kwargs))
        self._log_to_file('ERROR', message, **kwargs)

    def suspicious(self, message: str, **kwargs):
        # self.logger.error(self._format_message(message, **kwargs))
        self._log_to_file('SUSPICIOUS', message, **kwargs)

    def _format_message(self, level: str, message: str, timestamp: str, **kwargs):
        custom_info = " ".join(
            f"{key}={value}," for key, value in kwargs.items())
        return f"{level} - [{timestamp}] # {message} - {custom_info}"

    def _log_to_file(self, level: str, message: str, **kwargs):
        log_entry = Log
        current_utc_datetime = datetime.datetime.now(datetime.UTC)
        formatted_datetime = current_utc_datetime.strftime(
            "%Y-%m-%dT%H:%M:%S.%f")[:-4]+'Z'
        log_entry.timestamp = formatted_datetime
        log_entry.level = level
        log_entry.message = message
        log_entry.kwargs = kwargs
        log_entry.str_repr = self._format_message(
            level, message, formatted_datetime, **kwargs)
        encrypted_log_entry = self._encoder.encrypt_json(
            Log.to_json(log_entry))

        if os.path.exists(self.encrypted_log_file):
            self._encoder.decrypt_file(self.encrypted_log_file)

        with open(self.log_file, 'a') as file:
            file.write(f"{encrypted_log_entry}\n")

        self._encoder.encrypt_file(self.log_file)

    def read_logs(self):
        logs = []

        if os.path.exists(self.encrypted_log_file):
            self._encoder.decrypt_file(self.encrypted_log_file)

        with open(self.log_file, 'r') as file:
            for line in file:
                log_line = self._encoder.decrypt_json(
                    line.encode('utf-8'))
                logs.append(Log.from_json(log_line))
        if os.path.exists(self.log_file):
            self._encoder.encrypt_file(self.log_file)
        logs.reverse()
        return logs
