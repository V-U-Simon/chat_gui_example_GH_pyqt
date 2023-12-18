"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только последний
октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.
"""


import subprocess
import ipaddress


def host_range_ping(start_ip, range_size):
    start_ip = ipaddress.ip_address(start_ip)
    for i in range(range_size):
        # Create the next IP address by adding i to the last octet
        ip = start_ip + i
        try:
            # Ping the IP address
            response = subprocess.run(
                ["ping", "-c", "1", "-W", "1", str(ip)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # Check if the ping was successful
            if response.returncode == 0:
                print(f"Узел {ip} доступен")
            else:
                print(f"Узел {ip} недоступен")
        except Exception as e:
            print(f"Ошибка при попытке доступа к {ip}: {e}")


# Example usage
host_range_ping("192.168.1.1", 10)
