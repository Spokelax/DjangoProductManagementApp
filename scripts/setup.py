import subprocess
import sys
import time

from colorama import Fore, Style, init
from loguru import logger

# Initialize colorama for Windows compatibility
init()


# TODO: Document me
def run_command(command: list[str], error_message: str, *args, **kwargs) -> bool:
    use_logger = kwargs.get("useLogger", True)
    start_time = time.time()
    process = None

    if use_logger:
        logger.info(f"Executing: {' '.join(command)}")

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
                if use_logger:
                    logger.info(f"{Fore.GREEN}| {line.strip()}{Style.RESET_ALL}")
                else:
                    print(line.strip())

        stderr = process.stderr.read().strip()
        return_code = process.wait()

        if return_code != 0:
            if use_logger:
                logger.error(f"{error_message}: {stderr}")
            else:
                print(f"Error: {error_message}: {stderr}", file=sys.stderr)
            return False

        if use_logger:
            logger.info(f"Completed in {(time.time() - start_time):.2f} seconds")
        return True

    except Exception as e:
        if use_logger:
            logger.error(f"{error_message}: {str(e)}")
        else:
            print(f"Error: {error_message}: {str(e)}", file=sys.stderr)
        return False

    finally:
        if process:
            process.stdout.close()
            process.stderr.close()


# TODO: Document me
def create_superuser() -> bool:
    logger.info("Starting superuser creation")
    try:
        logger.info(
            f"{Fore.YELLOW}Follow the prompts to create a superuser (or press Ctrl+C to skip){Style.RESET_ALL}"
        )
        subprocess.run(
            ["pdm", "run", "python", "src/manage.py", "createsuperuser"],
            check=True,
            text=True,
        )
        logger.info("Superuser created successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create superuser: {e.stderr}")
        return False
    except KeyboardInterrupt:
        logger.warning("Superuser creation skipped by user")
        return True  # Treat skip as success to continue script


# TODO: Document me
def main():
    logger.info(f"{Fore.GREEN}---- Starting Django Setup ----{Style.RESET_ALL}")

    # Step 1: Run migrations
    logger.info(f"{Fore.GREEN}---- (1/5) Running Migrations ----{Style.RESET_ALL}")
    if not run_command(
        ["pdm", "run", "python", "src/manage.py", "makemigrations"],
        "Failed to create migrations",
    ):
        return
    if not run_command(
        ["pdm", "run", "python", "src/manage.py", "migrate"],
        "Failed to apply migrations",
    ):
        return

    # Step 2: Generate static files (assuming preparation or no-op if no build step)
    logger.info(f"{Fore.GREEN}---- (2/5) Generating Static Files ----{Style.RESET_ALL}")
    logger.info("No custom static file generation step defined. Skipping.")

    # Step 3: Collect static files
    logger.info(f"{Fore.GREEN}---- (3/5) Collecting Static Files ----{Style.RESET_ALL}")
    if not run_command(
        ["pdm", "run", "python", "src/manage.py", "collectstatic", "--noinput"],
        "Failed to collect static files",
    ):
        return

    # Step 4: Create superuser
    logger.info(f"{Fore.GREEN}---- (4/5) Creating Superuser ----{Style.RESET_ALL}")
    if not create_superuser():
        return

    # Step 5: Print PDM scripts
    logger.info(f"{Fore.GREEN}---- (5/5) Listing PDM Scripts ----{Style.RESET_ALL}")

    if not run_command(
        ["pdm", "run", "-l"], "Failed to list PDM scripts", useLogger=False
    ):
        return

    logger.info(f"{Fore.GREEN}---- Django Setup Complete ----{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
