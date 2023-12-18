"""
4. Продолжаем работать над проектом «Мессенджер»:
a) Реализовать скрипт, запускающий два клиентских приложения: на чтение чата и на запись в него. Уместно использовать
модуль subprocess).
b) Реализовать скрипт, запускающий указанное количество клиентских приложений.
"""

from subprocess import call, Popen
import threading


# COMMAND_RUN_SERVER = ["python", "./hello.py"]
COMMAND_RUN_SERVER = ["python", "./messenger/server.py"]
COMMAND_RUN_CLIENT = ["python", "./messenger/client.py"]


def start_server():
    call(COMMAND_RUN_SERVER, shell=False)


def create_client():
    Popen(COMMAND_RUN_CLIENT, shell=False)


def start_clients(qty: int = 2):
    threads = []
    for i in range(qty):
        threads.append(threading.Thread(target=create_client))
        threads[i].start()
    return threads


if __name__ == "__main__":
    threading.Thread(target=start_server).start()
    # threading.Thread(target=start_clients).start()
