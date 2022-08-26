from subprocess import run
from time import sleep

# Path and name to the script you are trying to start
file_path = "app.py"
restart_timer = 0.5


def start_script():
    try:
        # Make sure 'python' command is available
        # venv\Scripts\python.exe
        run("venv\Scripts\pythonw.exe "+file_path, check=True)
    except:
        # Script crashed, lets restart it!
        handle_crash()


def handle_crash():
    sleep(restart_timer)
    start_script()


start_script()
