# Пример использования subprocess.call
import subprocess

# Запуск команды 'ls' (список файлов в текущей директории) с помощью subprocess.call
code = subprocess.call(["ls", "-l"])
# return_code_call = subprocess.call(["./hello.py"])

# # Пример использования subprocess.run
# # Запуск той же команды 'ls' с помощью subprocess.run
# result_run = subprocess.run(["./hello"], capture_output=True, text=True)


# # Пример использования subprocess.Popen
# # Запуск команды 'ls' с помощью subprocess.Popen
# process = subprocess.Popen(["ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# stdout, stderr = process.communicate()

# print(return_code_call, result_run.stdout, stdout.decode())  # Возвращаем результаты

print()

completed_process = subprocess.run(["ls", "-l"])
completed_process.stdout
completed_process.stderr


print()

process = subprocess.Popen(["ls", "-l"])

print(process.stdout)
print(process.stdout)
