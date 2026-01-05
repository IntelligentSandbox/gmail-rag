import venv
import subprocess
import os

# https://docs.python.org/3/library/venv.html
venv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
if not os.path.exists(venv_dir):
    venv.create(venv_dir, with_pip=True)
subprocess.check_call([f"{venv_dir}/bin/pip", "install", "-r", "src/requirements.txt"])
print(f"run: source {venv_dir}/bin/activate")
