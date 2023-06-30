import json
import subprocess
import os
import logging
import select
import subprocess
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')

# Define the companies and their corresponding numbers
COMPANIES = {
    'company1': 1,
    'company2': 2
}

services = {
    'frontend': 0,
    'backend': 0,
    'algs1': 0,
    'algs2': 0
}

def load_config():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.exception(f"Failed to load config file: {e}")
        return None


def execute_command(command, cwd):
    if isinstance(command, str):
        command = command.split()

    try:
        return subprocess.call(command, cwd=cwd) == 0
    except subprocess.CalledProcessError as e:
        logger.exception(f"Failed to execute command '{command}' in {cwd}: {e}")
        return False

def get_container_names(company, service):
    config = load_config()
    return config.get(company, {}).get(service, {}).get('containers', [])

def is_container_running(container_name):
    command = f"docker ps --filter name=^/{container_name}$"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return container_name in output

def is_image_built(image_name):
    command = f"docker images --filter reference={image_name}"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return image_name in output

def build_service(company, service):
    config = load_config()
    if config is None:
        logger.error("No config found. Aborting build process.")
        return

    build_command = config.get(company, {}).get(service, {}).get('build', None)
    if build_command is None:
        logger.warning(f"No build command found for {service} in {company}. Skipping build process.")
        return

    repo_dir = os.path.join(SCRIPT_DIR, company, service)
    if not os.path.exists(repo_dir):
        logger.warning(f"Could not find {service} in {company}. Skipping build process.")
        return

    # Execute build command and get the return code
    if execute_command(build_command, cwd=repo_dir):
        logger.info(f"Successfully built {service} in {company}")
    else:
        logger.error(f"Failed to build {service} in {company}")


def build_all():
    logger.info("Building services...")

    for company in COMPANIES:
        for service in services:
            build_service(company, service)

    logger.info("Building complete!")


def kill_service(service_name):
    if service_name not in services:
        logger.error(f"Invalid service name: {service_name}. Not killing any services.")
        return False

    current_company = 'company' + str(services[service_name])

    if current_company in COMPANIES.keys():
        container_names = get_container_names(current_company, service_name)

        for container_name in container_names:
            stop_command = ["docker", "container", "stop", container_name]
            remove_command = ["docker", "container", "rm", container_name]

            if execute_command(stop_command, SCRIPT_DIR):
                logger.info(f"Stopped Docker container {container_name}.")
            else:
                logger.error(f"Failed to stop Docker container {container_name}.")
                return

            if execute_command(remove_command, SCRIPT_DIR):
                logger.info(f"Removed Docker container {container_name}.")
            else:
                logger.error(f"Remove Docker container {container_name}.")
                return
                
        services[service_name] = 0
        return True

    logger.info(f"No company is currently running the {service_name} service.")
    return False


def kill_all_services():
    logger.info("Killing all services...")

    for service in services:
        logger.info(f"Killing service: {service}")
        kill_service(service)

    logger.info("All services have been killed.")



def run_service(company, service):
    if service not in services:
        logger.error(f"Invalid service name: {service}. Skipping...")
        return

    current_running_company = services[service]
    if current_running_company == company:
        logger.info(f"Company {company} is already running {service}. Skipping...")
        return

    # If the current running service is not from the same company,
    # kill the service before starting the new one
    if current_running_company != 0:
        kill_service(service)

    config = load_config()
    if config is None:
        logger.error("Error: Could not load config.")
        return

    run_command = config.get(f"company{company}", {}).get(service, {}).get('run')
    repo_dir = os.path.join(SCRIPT_DIR, f"company{company}", service)

    if os.path.exists(repo_dir):
        container_names = config.get(f"company{company}", {}).get(service, {}).get('containers')
        
        for container_name in container_names:
            if is_container_running(container_name):
                logger.info(f"Container for {service} in {company} already running.")
            else:
                if execute_command(run_command, repo_dir):
                    break
                else:
                    logger.error(f"Failed to run command '{run_command}' in {repo_dir}")
    else:
        logger.warning(f"Could not find {service} in company{company}. Skipping...")

    services[service] = company


def run_services(service_companies: list):
    logger.info("Starting containers...")

    for service, company in zip(services.keys(), service_companies):
        run_service(company, service)

    logger.info("Completed starting containers!")


def run_company(company):
    if company not in COMPANIES.values():
        logger.error("Invalid company number provided. Expected 1 or 2.")
        return 1

    try:
        print("Running company {}".format(company))
        run_services([company] * len(services))
    except Exception as e:
        logger.exception(f"Error running services: {e}")
        return 1

    return 0

def swap_service(service_name):
    if service_name not in services:
        logger.error(f"Invalid service name: {service_name}. Not swapping.")
        return False

    # The company currently running the service
    current_company = services[service_name]
    # The total number of companies
    num_companies = len(COMPANIES)

    # The company that should run the service next
    next_company = (current_company % num_companies) + 1

    # Stop the service for the current company
    if not kill_service(service_name):
        logger.warning(f"Failed to kill {service_name} for company{current_company}.")
        return False

    # Start the service for the next company
    if run_service(f"{next_company}", service_name):
        logger.warning(f"Failed to start {service_name} for company{next_company}.")
        return False

    # Update the company running the service
    services[service_name] = next_company
    logger.info(f"Successfully swapped {service_name} to company{next_company}.")
    return True



def clone_service(company_name, service):
    config = load_config()
    if config is None:
        logger.error("Error: Could not load config.")
        return

    clone_command = config.get(company_name, {}).get(service, {}).get('clone')
    if clone_command:
        repo_dir = os.path.join(SCRIPT_DIR, company_name, service)
        if not os.path.exists(repo_dir):
            if not execute_command(clone_command, SCRIPT_DIR):
                logger.error(f"Failed to clone {service} of {company_name} from command: {clone_command}")
        else:
            logger.info(f"{service} already exists in {company_name}. Pulling instead...")
            if not execute_command("git pull", repo_dir):
                logger.error(f"Failed to clone {service} of {company_name} from command: {clone_command}")

    else:
        logger.warning(f"No clone command found for {service} in {company_name}. Skipping cloning...")


def is_service_cloned(company, service):
    repo_dir = os.path.join(SCRIPT_DIR, company, service)
    return os.path.exists(repo_dir) and bool(os.listdir(repo_dir))


def clone_all_services():
    for company in COMPANIES:
        for service in services:
            if not is_service_cloned(company, service):
                clone_service(company, service)


def test():
    logger.info("This has not been implemented yet")


def autotest_all():
    logger.info("This has not been implemented yet")


def handle_run(args):
    if len(args) != 1:
        logger.info("Usage: run [1 or 2]")
    else:
        try:
            run_company(int(args[0]))
        except ValueError:
            logger.error("Invalid company number. Please provide 1 or 2.")


def handle_runfrom(args):
    if len(args) != 4:
        logger.info("Usage: runfrom [frontend] [backend] [algs1] [algs2]")
        logger.info("For each service provide a 1 or 2 to indicate which company to run from.")
    else:
        run_services(list(map(int, args)))


def handle_swap(args):
    if len(args) != 1:
        logger.info("Usage: swap 'frontend' or 'backend' or 'algs1' or 'algs2'")
    else:
        if not swap_service(args[0]):
            logger.warning(f"Failed to swap {args[0]}")


def handle_exit(args):
    kill_all_services()
    exit(0)


def handle_test(args):
    test()


def handle_testall(args):
    autotest_all()


def handle_help(args):
    print_help()


COMMAND_HANDLERS = {
    'run': handle_run,
    'runfrom': handle_runfrom,
    'swap': handle_swap,
    'exit': handle_exit,
    'test': handle_test,
    'testall': handle_testall,
    'help': handle_help,
}


def parse_input(user_input):
    split_input = user_input.split()

    if len(split_input) == 0:
        logger.info("Please provide a valid command.")
        print_help()
        return

    command = split_input[0]
    args = split_input[1:]

    handler = COMMAND_HANDLERS.get(command)
    if handler is None:
        logger.error(f"Unknown command: {command}")
        print_help()
    else:
        handler(args)


def print_help():
    logger.info("""
    Available commands:
    - run [Company] - Runs all four services from a given company. Provide 1 or 2 for the company.
    - runfrom [Frontend] [Backend] [Algs1] [Algs2] - Runs services from each given company. For each service, provide 1 or 2 to indicate which company to run from.
    - swap [service] - Swaps the running service from one company to the other. Provide 'frontend' or 'backend' or 'algs1' or 'algs2' to indicate which service to swap.
    - exit - Terminate all running containers and exit the program.
    - test - Test the currently running containers. This has not been implemented yet.
    - testall - Run full test suite. This has not been implemented yet.
    - help - Show this help message.
    """)


def main():
    # Clone and build all services, if necessary
    clone_all_services()
    #build_all()

    # Run company 2 containers by default
    run_company(COMPANIES['company2'])

    while True:
        # Get user input
        user_input = input("Enter a command: ")
        parse_input(user_input)



if __name__ == "__main__":
    main()
