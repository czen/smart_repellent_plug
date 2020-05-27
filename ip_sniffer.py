import subprocess


def get_ip(mac):
    cmd = 'arp -a | findstr "%s" ' % mac
    returned_output = subprocess.check_output((cmd), shell=True, stderr=subprocess.STDOUT)
    # print(returned_output)
    parse = str(returned_output).split(' ', 1)
    ip = parse[1].split(' ')
    return ip[1]
