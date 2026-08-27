import os
import subprocess


def clearscreen():
    return subprocess.run("cls" if os.name == "nt" else "clear", check=False)
