# server

from messenger.common.utils import get_message, send_message
from messenger.decorators import Log
import messenger.errors_user as errors_user
import messenger.common.variables as variables

import sys
import argparse
import logging
import select
from collections import deque
from socket import socket, AF_INET, SOCK_STREAM


LOG = logging.getLogger("server")


class Server:
    RESPONSES = {
        "OK": {variables.RESPONSE: 200},
        "BAD_REQUEST": {variables.RESPONSE: 400, variables.ERROR: "Bad Request"},
    }

    @Log(LOG)
    def __init__(self):
        self.clients_names = dict()
        self.clients_list = []
        self.messages_deque = deque()
        self.receive_data_list = []
        self.send_data_list = []
        self.errors_list = []
        self.listen_port, self.listen_address = self.get_params()
        self.transport = self.prepare_socket()
        LOG.debug(f"Создан объект сервера")

    @Log(LOG)
    def prepare_socket(self):
        transport = socket(AF_INET, SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        transport.settimeout(2)
        transport.listen(variables.MAX_CONNECTIONS)
        LOG.info(
            f"Запущен сервер. Порт подключений: {self.listen_port}, адрес прослушивания: {self.listen_address}"
        )
        return transport

    @Log(LOG)
    def process_client_message(self, message, client):
        if (
            message.get(variables.ACTION) == variables.PRESENCE
            and variables.USER in message
            and variables.TIME in message
            and variables.PORT in message
        ):
            client_name = message[variables.USER][variables.ACCOUNT_NAME]
            if client_name not in self.clients_names:
                self.clients_names[client_name] = client
                send_message(client, self.RESPONSES.get("OK"))
                LOG.debug(f"Клиент {client_name} зарегестрирован на сервере")
            else:
                response = self.RESPONSES["BAD_REQUEST"]
                response[
                    variables.ERROR
                ] = f"Имя пользователя {client_name} уже занято."
                send_message(client, response)
                self.clients_list.remove(client)
                client.close()
                LOG.error(
                    f"Имя пользователя {client_name} уже занято. Клиент отключён."
                )
            return

        if (
            message.get(variables.ACTION) == variables.MESSAGE
            and variables.MESSAGE_TEXT in message
            and variables.SENDER in message
            and variables.DESTINATION in message
            and message.get(variables.DESTINATION) in self.clients_names
        ):
            self.messages_deque.append(message)
            LOG.debug(
                f"Сообщение клиента {message[variables.SENDER]} "
                f"для клиента {message[variables.DESTINATION]} добавлено в очередь сообщений"
            )
            return

        if (
            message.get(variables.ACTION) == variables.EXIT
            and variables.ACCOUNT_NAME in message
        ):
            self.clients_list.remove(
                self.clients_names[message[variables.ACCOUNT_NAME]]
            )
            self.clients_names[message[variables.ACCOUNT_NAME]].close()
            LOG.debug(
                f"Клиент {message[variables.ACCOUNT_NAME]} вышел из чата. Клиент отключён от сервера."
            )
            del self.clients_names[message[variables.ACCOUNT_NAME]]
            return

        send_message(client, self.RESPONSES.get("BAD_REQUEST"))
        return

    def received_messages_processing(self):
        for client_with_message in self.receive_data_list:
            try:
                self.process_client_message(
                    get_message(client_with_message), client_with_message
                )
            except Exception:
                LOG.info(
                    f"Клиент {client_with_message.getpeername()} отключился от сервера."
                )
                self.clients_list.remove(client_with_message)

    @Log(LOG)
    def send_messages_to_clients(self):
        while self.messages_deque:
            message = self.messages_deque.popleft()
            waiting_client = self.clients_names[message[variables.DESTINATION]]
            if waiting_client in self.send_data_list:
                try:
                    send_message(waiting_client, message)
                    LOG.info(
                        f"Сообщение клиента {message[variables.SENDER]} отправлено клиенту {message[variables.DESTINATION]}"
                    )
                except Exception:
                    LOG.info(
                        f"Клиент {waiting_client.getpeername()} отключился от сервера."
                    )
                    waiting_client.close()
                    self.clients_list.remove(waiting_client)

    def run(self):
        while True:
            try:
                client, client_address = self.transport.accept()
            except OSError:
                pass
            else:
                LOG.info(f"Установлено соедение с клиентом {client_address}")
                self.clients_list.append(client)

            self.receive_data_list = []
            self.send_data_list = []
            self.errors_list = []
            try:
                if self.clients_list:
                    (
                        self.receive_data_list,
                        self.send_data_list,
                        self.errors_list,
                    ) = select.select(self.clients_list, self.clients_list, [], 0)
            except OSError:
                pass

            self.received_messages_processing()

            if self.messages_deque and self.send_data_list:
                self.send_messages_to_clients()

    @staticmethod
    @Log(LOG)
    def get_params():
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", type=int, default=variables.DEFAULT_PORT)
        parser.add_argument("-a", type=str, default="")
        args = parser.parse_args()
        try:
            if not (1024 < args.p < 65535):
                raise errors_user.PortError
        except errors_user.PortError as error:
            LOG.critical(f"Ошибка порта {args.p}: {error}. Соединение закрывается.")
            sys.exit(1)
        return args.p, args.a


if __name__ == "__main__":
    server = Server()
    server.run()
