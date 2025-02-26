import subprocess


def get_ping_latency(host, num):
    result = subprocess.run(['ping', '-c', str(num), host], capture_output=True, text=True)

    for line in result.stdout.split("\n"):
        if "rtt min/avg/max/mdev" in line:
            stats = line.split('=')[1].strip().split('/')
            return float(stats[0]), float(stats[1]), float(stats[2])

def input_hosts():
    str = input('Введите адреса (google.com, 8.8.8.8, nsu.ru): ')
    return str.split(', ')


if __name__ == '__main__':
    host_list = input_hosts()
    number_of_requests = input('Введите количество запросов: ')

    for host in host_list:
        latency = get_ping_latency(host, number_of_requests)

        if latency:
            min, avg, max = latency
            print(f'Задержка до {host}: мин. {min} мс, сред. {avg} мс, макс. {max} мс')
        else:
            print(f'Не удалось получить задержку до {host}')