import os
import shutil
import subprocess
import venv
from datetime import datetime
from pathlib import Path
from time import time


# TODO: Document me
class Colors:
    GREEN = "\033[92m"
    GREEN_BACKGROUND = "\033[48;5;22m"
    GREY_BACKGROUND = "\033[48;5;235m"
    RED = "\033[91m"
    RED_BACKGROUND = "\033[48;5;196m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# TODO: Document me
# TODO: Type me
def logger(level, message) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = (
        Colors.GREEN
        if level == "INFO"
        else Colors.RED_BACKGROUND
        if level == "WARNING"
        else Colors.RED
    )
    print(
        f"{Colors.GREY_BACKGROUND}[{timestamp}]{Colors.RESET} {color}{level:5}{Colors.RESET}: {message}"
    )


# TODO: Document me
# TODO: Type me
def run(command, error_message) -> bool:
    logger("INFO", f"Executing: {' '.join(command)}")
    start_time = time()
    process = None
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        stdout_lines = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                stdout_lines.append(line.strip())
                print(line.strip())

        stderr = process.stderr.read().strip()
        return_code = process.wait()

        if return_code != 0:
            logger("ERROR", f"{error_message}: {stderr}")
            return False

        logger("INFO", f"Completed in {time() - start_time:.2f} seconds")
        return True

    except Exception as e:
        logger("ERROR", f"{error_message}: {str(e)}")
        return False
    finally:
        if process:
            process.stdout.close()
            process.stderr.close()


# TODO: Document me
def create_venv(venv_path: Path) -> bool:
    logger("INFO", f"Creating virtual environment at {venv_path}")
    try:
        venv.create(venv_path, with_pip=True, clear=True)
        logger("INFO", "Virtual environment created successfully")

        return True

    except Exception as e:
        logger("ERROR", f"Failed to create virtual environment: {str(e)}")
        logger(
            "ERROR", "This is likely due a process currently using the .venv directory."
        )
        logger(
            "ERROR",
            "Try killing any python processes and/or restart your IDE and waiting a few seconds.",
        )
        return False


# TODO: Document me
def main():
    print(f"{Colors.GREEN_BACKGROUND}---- Starting Pre-setup ----{Colors.RESET}")

    # Find root path
    root = Path(__file__).resolve().parent.parent
    if not root.is_dir():
        logger("WARN", f"{root} is not a directory.")
        return

    # Check if Python is installed
    if not run(
        ["python", "--version"], "Python is not installed. Please install Python."
    ):
        return

    print(
        f"{Colors.GREEN_BACKGROUND}---- (1/2) Creating Virtual Environment ----{Colors.RESET}"
    )

    # Verify that .venv does not exist
    venv_path = root / ".venv"
    if venv_path.exists():
        logger("ERROR", f"'{venv_path}' already exists, removing it.")

        # Delete the .venv directory
        try:
            shutil.rmtree(venv_path)
            logger("INFO", f"Removed {venv_path}")
        except OSError as e:
            logger("ERROR", f"Failed to remove {venv_path}: {e}")
            return

    # Install virtualenv
    if not create_venv(venv_path):
        return

    # Get path to venv's Python executable
    venv_python = ""
    if os.environ.get("OS", "") != "Windows_NT":
        venv_python = str(venv_path / "bin" / "python")
    else:
        venv_python = str(venv_path / "Scripts" / "python.exe")

    if not Path(venv_python).exists():
        logger("ERROR", f"Virtual environment Python not found at {venv_python}.")
        return

    # If not Windows, add executable permission to activate script
    if os.environ.get("OS", "") != "Windows_NT":
        activate_script = venv_path / "bin" / "activate"
        if not os.access(activate_script, os.X_OK):
            logger("INFO", f"Setting executable permission for {activate_script}")
            try:
                os.chmod(activate_script, 0o755)
                logger("INFO", f"Set executable permission for {activate_script}")
            except Exception as e:
                logger("ERROR", f"Failed to set executable permission: {e}")
                return

    print(f"{Colors.GREEN_BACKGROUND}---- (2/2) PDM Install ----{Colors.RESET}")

    # Install PDM in the virtual environment
    if not run(
        [venv_python, "-m", "pip", "install", "pdm>=2.21.1"],
        "Failed to install PDM",
    ):
        return

    # Install PDM dependencies
    if not run(
        [venv_python, "-m", "pdm", "sync"],
        "Failed to install PDM dependencies",
    ):
        return

    logger(
        "INFO",
        "PDM setup complete. To use 'pdm' commands directly, activate the virtual environment:",
    )
    logger("INFO", f"  {Colors.MAGENTA}├──{Colors.RESET} Windows")
    logger(
        "INFO",
        f"  {Colors.MAGENTA}│   ├──{Colors.RESET} CMD:        {venv_path}\\Scripts\\activate.bat",
    )
    logger(
        "INFO",
        f"  {Colors.MAGENTA}│   └──{Colors.RESET} PowerShell: {venv_path}\\Scripts\\Activate.ps1",
    )
    logger(
        "INFO",
        f"  {Colors.MAGENTA}└──{Colors.RESET} Unix/Linux: source {venv_path}/bin/activate",
    )

    print(f"\n{Colors.GREEN_BACKGROUND}---- PDM Setup Complete ----{Colors.RESET}")


if __name__ == "__main__":
    main()
