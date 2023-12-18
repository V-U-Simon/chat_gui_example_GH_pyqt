"""
3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate). Таблица должна состоять из двух колонок
"""

import subprocess
import ipaddress
from tabulate import tabulate


def host_range_ping(start_ip, range_size):
    start_ip = ipaddress.ip_address(start_ip)
    results = []

    for i in range(range_size):
        ip = start_ip + i
        try:
            # Ping the IP address with a timeout
            response = subprocess.run(
                ["ping", "-c", "1", "-W", "1", str(ip)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # Determine status
            status = "Доступен" if response.returncode == 0 else "Недоступен"
            results.append((str(ip), status))
        except Exception as e:
            results.append((str(ip), f"Ошибка: {e}"))

    return results


def host_range_ping_tab(start_ip, range_size):
    results = host_range_ping(start_ip, range_size)
    print(tabulate(results, headers=["IP адрес", "Статус"]))


if __name__ == "__main__":
    host_range_ping_tab("192.168.1.1", 10)

"""
IP адрес      Статус
------------  ----------
192.168.1.1   Доступен
192.168.1.2   Недоступен
192.168.1.3   Доступен
192.168.1.4   Доступен
192.168.1.5   Недоступен
192.168.1.6   Недоступен
192.168.1.7   Недоступен
192.168.1.8   Недоступен
192.168.1.9   Недоступен
192.168.1.10  Недоступен
"""
