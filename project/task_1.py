"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения («Узел
доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""

import subprocess
import ipaddress
import socket


def host_ping(hosts):
    for host in hosts:
        try:
            # Convert hostname to IP address
            ip = ipaddress.ip_address(socket.gethostbyname(host))
            # Ping the IP address
            response = subprocess.run(
                ["ping", "-c", "1", "-W", "2", str(ip)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Check if the ping was successful
            if response.returncode == 0:
                print(f"Узел {host} доступен")
            else:
                print(f"Узел {host} недоступен")

        except ValueError:
            print(f"{host} не является допустимым IP-адресом или именем хоста")
        except Exception as e:
            print(f"Ошибка при попытке доступа к {host}: {e}")


# Example usage

if __name__ == "__main__":
    host_ping(["192.168.1.10", "google.com", "192.168.1.1"])
