# Starter

import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие: q / quit - выход, '
                   's / start - запустить сервер и клиенты, x / close - закрыть все окна: ')

    if ACTION == 'q' or ACTION == 'quit':
        break
    elif ACTION == 's' or ACTION == 'start':
        PROCESS.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m send',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m listen',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x' or ACTION == 'close':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()