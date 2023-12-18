#  Константы

DEFAULT_PORT = 7777                 # Порт поумолчанию для сетевого ваимодействия
DEFAULT_IP_ADDRESS = '127.0.0.3'    # IP адрес по умолчанию для подключения клиента
MAX_CONNECTIONS = 5                 # Максимальная очередь подключений
MAX_PACKAGE_LENGTH = 1024           # Максимальная длинна сообщения в байтах
ENCODING = 'utf-8'                  # Кодировка проекта

# Main keys of JIM protocol:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PORT = 'port'
SENDER = 'sender'

# Other keys which we use in protocol:
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
RESPONDEFAULT_IP_ADDRESSSE = 'respondefault_ip_addressse'
EXIT = 'exit'
DESTINATION = 'destination'

# Logging
LOG_DIRECTORY = 'data'
LOG_CLIENT_NAME = 'client.log'
LOG_SERVER_NAME = 'server.log'