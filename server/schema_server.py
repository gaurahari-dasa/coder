import socket
import subprocess

def _get_random_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run():
    port = _get_random_available_port()
    php_command = ["php", "-S", f"localhost:{port}", "-t", "schema-server"]
    process = subprocess.Popen(php_command)
    return port
