from enum import Enum
import json
import subprocess
import os
import logging
import subprocess
import time
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')

# Define the companies and services
class Company(Enum):
    none = 0
    company1 = 1
    company2 = 2

class Service(Enum):
    frontend = 1
    backend = 2
    algs1 = 3
    algs2 = 4

companies = [
    Company.company1,
    Company.company2
]

# Which company is running each service
services = {
    Service.frontend: Company.none,
    Service.backend: Company.none,
    Service.algs1: Company.none,
    Service.algs2: Company.none
}

# Backend env variable constants
company1_backend_algs1 = {
    Company.company1 : "http://host.docker.internal:5001,http://host.docker.internal:5001",
    Company.company2 : "http://host.docker.internal:8017,http://host.docker.internal:8017"
}

company1_backend_algs2 = {
    Company.company1 : "http://host.docker.internal:8080,http://host.docker.internal:8080",
    Company.company2 : "http://host.docker.internal:8001,http://host.docker.internal:8001"
}

company2_backend_algs1 = {
    Company.company1 : "http://host.docker.internal:5001/generate",
    Company.company2 : "http://host.docker.internal:8017/generate"
}

company2_backend_algs2 = {
    Company.company1 : "http://host.docker.internal:8080/predict",
    Company.company2 : "http://host.docker.internal:8001/predict"
}

def write_env_file(env_file_path, env_variables):
    with open(env_file_path, "w") as f:
        for key in env_variables:
            f.write(f'{key}={env_variables[key]}\n')

def set_frontend_env_variables():
    env_variables = {
        "REACT_APP_BACKEND_URL" : "http://localhost:8000"
    }
    write_env_file("company2/frontend/.env", env_variables)

def set_company1_env_variables(algs1_link: str, algs2_link: str):
    env_variables = {
        "DATABASE_URI" : "postgresql+psycopg2://admin:password@db:5432/uvic",
        "APP_SETTINGS" : "ProductionConfig",
        "FLASK_RUN_HOST" : "0.0.0.0",
        "FLASK_APP" : "app.py",
        "FLASK_DEBUG" : "1",
        "APP_VERSION" : "1.0.0",
        "ALG1_URLs" : f"{algs1_link}",
        "ALG2_URLs" : f"{algs2_link}"
    }
    write_env_file("company1/backend/.env", env_variables)

def set_company2_env_variables(algs1_link: str, algs2_link: str):
    env_variables = {
        "ENVIRONMENT" : "development",
        "MONGO_LOCAL_HOST" : "10.9.0.3:27017",
        "MONGO_LOCAL_USERNAME" : "admin",
        "MONGO_LOCAL_PASSWORD" : "admin",
        "ADMIN_1" : "rich.little",
        "ADMIN_2" : "dan.mai",
        "JWT_SECRET" : "secret",
        "API_HASH" : "fe80decbd03b2933f3d7eba3079e6b3e7c1bb2e3613f3671388c969fd6cd5aca",
        "ALGS1_API" : f"{algs1_link}",
        "ALGS2_API" : f"{algs2_link}"
    }
    write_env_file("company2/backend/.env", env_variables)

def set_company2_algs1_env_variables():
    env_variables = {
        "DJANGO_MODE" : "dev",
        "SECRET_KEY" : "4104c7d331cb642a222340cd5324b4f2",
        "HOST_NAME" : "host.docker.internal"
    }
    write_env_file("company2/algs1/.env", env_variables)

def set_company1_algs2_env_variables():
    env_variables = {
        "PORT": "8080",
        "BACKEND_URL": "http://host.docker.internal:8000/schedules/prev"
    }
    write_env_file("company1/algs2/.env", env_variables)

def set_company2_algs2_env_variables():
    env_variables = {
        "DJANGO_MODE" : "dev",
        "SECRET_KEY" : "4104c7d331cb642a222340cd5324b4f2",
        "HOST_IP" : "127.0.0.1",
        "HOST_NAME" : "host.docker.internal",
        "BACKEND_URL" : "http://host.docker.internal:8000"
    }
    write_env_file("company2/algs2/.env", env_variables)

def update_backend_env_variables(backend: Company, algs1: Company, algs2: Company):
    if backend == Company.company1:
        set_company1_env_variables(company1_backend_algs1[algs1], company1_backend_algs2[algs2])
    else:
        set_company2_env_variables(company2_backend_algs1[algs1], company2_backend_algs2[algs2])

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

def get_container_names(company: Company, service: Service):
    config = load_config()
    return config.get(company.name, {}).get(service.name, {}).get('containers', [])

def is_container_running(container_name: str):
    command = f"docker ps --filter name=^/{container_name}$"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return container_name in output

def is_image_built(image_name: str):
    command = f"docker images --filter reference={image_name}"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return image_name in output

def build_service(company: Company, service: Service):
    config = load_config()
    if config is None:
        logger.error("No config found. Aborting build process.")
        return

    build_command = config.get(company.name, {}).get(service.name, {}).get('build', None)
    if build_command is None:
        logger.warning(f"No build command found for {service.name} in {company.name}. Skipping build process.")
        return

    repo_dir = os.path.join(SCRIPT_DIR, company.name, service.name)
    if not os.path.exists(repo_dir):
        logger.warning(f"Could not find {service.name} in {company.name}. Skipping build process.")
        return

    # Execute build command and get the return code
    if execute_command(build_command, cwd=repo_dir):
        logger.info(f"Successfully built {service.name} in {company.name}")
    else:
        logger.error(f"Failed to build {service.name} in {company.name}")


def build_all():
    logger.info("Building services...")

    for company in companies:
        for service in Service:
            build_service(company, service)

    logger.info("Building complete!")


def kill_service(service: Service):
    current_company = services[service]

    if current_company == Company.none:
        logger.info(f"No company is currently running the {service.name} service.")
        return True
    repo_dir = os.path.join(SCRIPT_DIR, current_company.name, service.name)
    command = "docker-compose down"

    if not execute_command(command, repo_dir):
        logger.error(f"Failed to run command '{command}' in {repo_dir}")
        return False
    
    services[service] = Company.none
    return True


def kill_all_services():
    logger.info("Killing all services...")

    for service in Service:
        if services[service] != Company.none:
            logger.info(f"Killing service: {service}")
            kill_service(service)

    logger.info("All services have been killed.")


def run_service(company: Company, service: Service):
    current_company = services[service]
    if current_company == company:
        logger.info(f"Company {company.name} is already running {service.name}. Skipping...")
        return True

    # If the current running service is not from the same company,
    # kill the service before starting the new one
    if current_company != Company.none:
        if kill_service(service):
            services[service] = Company.none


    config = load_config()
    if config is None:
        logger.error("Error: Could not load config.")
        return False

    run_command = config.get(company.name, {}).get(service.name, {}).get('run')
    repo_dir = os.path.join(SCRIPT_DIR, company.name, service.name)

    if not os.path.exists(repo_dir):
        logger.warning(f"Could not find {service.name} in {company.name}. Skipping...")
        return False
    
    if not execute_command(run_command, repo_dir):
        logger.error(f"Failed to run command '{run_command}' in {repo_dir}")
        return False

    services[service] = company
    return True


def run_services(service_companies: dict[Service, Company]):
    logger.info("Updating backend env variables...")
    kill_service(Service.backend)
    update_backend_env_variables(service_companies[Service.backend], service_companies[Service.algs1], service_companies[Service.algs2])
    build_service(service_companies[Service.backend], Service.backend)

    logger.info("Starting containers...")
    for service, company in service_companies.items():
        run_service(company, service)

    logger.info("Completed starting containers!")


def run_company(company: Company):
    logger.info(f"Running all services for {company.name}...")
    try:
        run_services({Service.frontend: company, Service.backend: company, Service.algs1: company, Service.algs2: company})
    except Exception as e:
        logger.exception(f"Error running services: {e}")
        return False

    return True

def swap_service(service: Service):
    # The company currently running the service
    current_company = services[service]
    # The total number of companies
    num_companies = len(companies)

    # The company that should run the service next
    next_company = Company((current_company.value % num_companies) + 1)

    # Stop the service for the current company
    if not kill_service(service):
        logger.info(f"Failed to kill {service.name} for {current_company.name}")

    # Start the service for the next company
    if not run_service(next_company, service):
        logger.warning(f"Failed to start {service.name} for {next_company.name}")
        return False

    # Update the company running the service
    services[service] = next_company
    logger.info(f"Successfully swapped {service.name} to {next_company.name}")

    # Change backend env variables for swapped service only if all services are running
    if services[Service.frontend] != Company.none and services[Service.backend] != Company.none and services[Service.algs1] != Company.none and services[Service.algs2] != Company.none:
        logger.info(f"Updating backend env variables for {service.name} to {next_company.name}...")
        backend_company = services[Service.backend]
        kill_service(Service.backend)
        update_backend_env_variables(backend_company, services[Service.algs1], services[Service.algs2])
        if not run_service(backend_company, Service.backend):
            logger.warning(f"Failed to start backend for {backend_company.name}")
            return False

    return True

def clone_service(company: Company, service: Service):
    config = load_config()
    if config is None:
        logger.error("Error: Could not load config.")
        return False

    clone_command = config.get(company.name, {}).get(service.name, {}).get('clone')
    if not clone_command:
        logger.warning(f"No clone command found for {service.name} in {company.name}. Skipping cloning...")
        return False

    repo_dir = os.path.join(SCRIPT_DIR, company.name, service.name)
    if not is_service_cloned(company, service):
        if not execute_command(clone_command, SCRIPT_DIR):
            logger.error(f"Failed to clone {service.name} of {company.name} from command: {clone_command}")
            return False
    else:
        logger.info(f"{service.name} already exists in {company.name}. Pulling instead...")
        if not execute_command("git pull", repo_dir):
            logger.error(f"Failed to pull {service.name} of {company.name} from command: {clone_command}")
            return False
    return True


def is_service_cloned(company: Company, service: Service):
    repo_dir = os.path.join(SCRIPT_DIR, company.name, service.name)
    return os.path.exists(repo_dir) and bool(os.listdir(repo_dir))


def clone_all_services():
    logger.info("Clonning all repositories...")
    for company in companies:
        for service in Service:
            if not clone_service(company, service):
                logger.error(f"Failed to clone {service.name} of {company.name}")
    
    logger.info("Completed clonning all repositories...")


def test():
    logger.info("This has not been implemented yet")


def autotest_all():
    # Run company 2 frontend for all tests
    run_service(Company.company2, Service.frontend)

    # Run every combination of company 1 and 2 for backend, algs1 and algs2
    for backend_company in companies:
        if services[Service.backend] != backend_company:
            swap_service(Service.backend)
        for algs1_company in companies:
            if services[Service.algs1] != algs1_company:
                swap_service(Service.algs1)
            for algs2_company in companies:
                if services[Service.algs2] != algs2_company:
                    swap_service(Service.algs2)
                logger.info("Waiting for services to be ready...")
                time.sleep(90)
                logger.info(f"Running tests for {backend_company.name} backend, {algs1_company.name} algs1 and {algs2_company.name} algs2...")
                test()

    logger.info("Finished all combinations of Company 1 and 2 tests")


def handle_run(args):
    if len(args) != 1:
        logger.info("Usage: run [1 or 2]")
    else:
        try:
            run_company(Company(int(args[0])))
        except ValueError:
            logger.error("Invalid company number. Please provide 1 or 2.")


def handle_runfrom(args):
    if len(args) != 4:
        logger.info("Usage: runfrom [frontend] [backend] [algs1] [algs2]")
        logger.info("For each service provide a 1 or 2 to indicate which company to run from.")
    else:
        run_services({Service.frontend: Company(int(args[0])), Service.backend: Company(int(args[1])), Service.algs1: Company(int(args[2])), Service.algs2: Company(int(args[3]))})


def handle_swap(args):
    if len(args) != 1:
        logger.info("Usage: swap 'frontend' or 'backend' or 'algs1' or 'algs2'")
        return
    
    try:
        service = Service[args[0]]
    except KeyError:
        logger.error(f"Unknown service: {args[0]}")
        return
    
    if not swap_service(service):
        logger.warning(f"Failed to swap {service._name_}")


def handle_killall(args):
    kill_all_services()

def handle_exit(args):
    kill_all_services()
    exit(0)


def handle_test(args):
    test()


def handle_testall(args):
    kill_all_services()
    autotest_all()


def handle_help(args):
    print_help()


COMMAND_HANDLERS = {
    'run': handle_run,
    'runfrom': handle_runfrom,
    'swap': handle_swap,
    'killall': handle_killall,
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
    - killall - Terminate all running containers.
    - exit - Terminate all running containers and exit the program.
    - test - Test the currently running containers. This has not been implemented yet.
    - testall - Run full test suite. This has not been implemented yet.
    - help - Show this help message.
    """)


def main():
    # Clone all services, if necessary
    clone_all_services()

    # Init frontend env variable
    set_frontend_env_variables()
    set_company1_algs2_env_variables()
    set_company2_algs1_env_variables()
    set_company2_algs2_env_variables()

    # set backend env variables
    # algs1 and algs2 are fixed in runtime
    update_backend_env_variables(Company.company1, Company.company1, Company.company1)
    update_backend_env_variables(Company.company2, Company.company2, Company.company2)

    # Build all services
    build_all()

    # Run company 2 containers by default
    # run_company(COMPANIES['company2'])

    print_help()

    while True:
        # Get user input
        user_input = input("Enter a command: ")
        parse_input(user_input)



if __name__ == "__main__":
    main()
