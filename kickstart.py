import subprocess
import time


def start_php_server():
    # Command to start the PHP server
    php_server_command = ["php", "-S", "localhost:8000", "-t", "webinterface"]

    # Start the PHP server as a subprocess
    php_server_process = subprocess.Popen(
        php_server_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("PHP server started on http://localhost:8000")
    return php_server_process


def start_python_server():
    # Command to start the Python server
    python_server_command = ["python3", "controller/controller.py"]

    # Start the Python server as a subprocess
    python_server_process = subprocess.Popen(
        python_server_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("Python server started")
    return python_server_process


def main():
    # Start the PHP server
    php_server_process = start_php_server()

    # Start the Python server
    python_server_process = start_python_server()

    try:
        # Keep the script running to keep the servers alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down servers...")
        # Terminate the PHP server
        php_server_process.terminate()
        # Terminate the Python server
        python_server_process.terminate()
        print("Servers have been shut down.")


if __name__ == "__main__":
    main()
