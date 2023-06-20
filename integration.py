import subprocess
import os

# Frontend, Backend, Algs1, Algs2
# 0 means neither, 1 means company 1 running, 2 means company 2 running
running = [2, 2, 2, 2]
script_dir = os.path.dirname(os.path.realpath(__file__))

def help():
    print("""
    Available commands:
    - run [Company] - Runs all four modules from a given company. Provide 1 or 2 for the company.
    - runfrom [Frontend] [Backend] [Algs1] [Algs2] - Runs modules from each given company. For each module, provide 1 or 2 to indicate which company to run from.
    - swap [Module] - Swaps the running module from one company to the other. Provide 'frontend' or 'backend' or 'algs1' or 'algs2' to indicate which module to swap.
    - exit - Terminate all running containers and exit the program.
    - test - Test the currently running containers. This has not been implemented yet.
    - testall - Run full test suite. This has not been implemented yet.
    """)

def run(company):
    global running, script_dir
    if not company in ['1', '2']:
        print("Invalid company number provided")
        return 1
    subprocess.run(["./shell/runfrom.sh", company, company, company, company], cwd=script_dir)
    running = [company, company, company, company]

def run_from(frontend_company, backend_company, algs1_company, algs2_company):
    global running, script_dir
    for module in [frontend_company, backend_company, algs1_company, algs2_company]:
        if not module in ['1', '2']:
            print("Invalid company number provided")
            return 1
    subprocess.run(["./shell/runfrom.sh", frontend_company, backend_company, algs1_company, algs2_company], cwd=script_dir)
    running = [frontend_company, backend_company, algs1_company, algs2_company]


def swap_module(module):
    global running, script_dir
    
    # Get the index of the module in the 'running' list
    module_dict = {'frontend': 0, 'backend': 1, 'algs1': 2, 'algs2': 3}
    module_index = module_dict.get(module)
    
    if module_index is None:
        print("Invalid module. Please provide 'frontend', 'backend', 'algs1', or 'algs2'")
        return

    # Kill the currently running module
    current_company = running[module_index]
    if current_company in [1, 2]:
        subprocess.run(["docker", "container", "stop", f"{module}_{current_company}"], cwd=script_dir)
        subprocess.run(["docker", "container", "rm", f"{module}_{current_company}"], cwd=script_dir)
    else:
        print("Could not get the company of the running module... Not killing any modules")

    # Determine the company to switch to
    # If company 1 is running, switch to company 2 and vice versa
    # If neither is running for the given module, run company 2
    new_company = 1 if running[module_index] == 2 else 2

    # Run the new module
    subprocess.run(["./shell/runfrom.sh", str(new_company), str(new_company), str(new_company), str(new_company)], cwd=script_dir) 

    # Update the 'running' list
    running[module_index] = new_company

    print(f"Switched {module} to company {new_company}")



def kill_all():
    global script_dir
    subprocess.run(['./shell/killall.sh'], cwd=script_dir)
    running = [0, 0, 0, 0]

def test():
    print("This has not been implemented yet")

def autotest_all():
    print("This has not been implemented yet")

def parse_input(user_input):
    split_input = user_input.split()

    if len(split_input) == 0:
        print("Please provide a valid command.")
        return

    command = split_input[0]

    if command == 'run':
        if len(split_input) != 2:
            print("Usage: run [1 or 2]")
        else:
            run(split_input[1])
    elif command == 'runfrom':
        if len(split_input) != 5:
            print("Usage: runfrom [frontend] [backend] [algs1] [algs2]")
            print("For each module provide a 1 or 2 to indicate which company to run from.")
        else:
            run_from(split_input[1], split_input[2], split_input[3], split_input[4])
    elif command == 'swap':
        if len(split_input) != 2:
            print("Usage: swap 'frontend' or 'backend' or 'algs1' or 'algs2'")
        else:
            swap_module(split_input[1])
    elif command == 'exit':
        kill_all()
        exit(0)
    elif command == 'test':
        test()
    elif command == 'testall':
        autotest_all()
    else:
        help()
        
        
def check_and_clone():
    global script_dir
    # List of directories to check
    dirs = [
        './company1/frontend',
        './company1/backend',
        './company1/algs1',
        './company1/algs2',
        './company2/frontend',
        './company2/backend',
        './company2/algs1',
        './company2/algs2',
    ]
    
    for dir in dirs:
        if not os.path.exists(os.path.join(script_dir, dir)):
            print(f"Directory {dir} does not exist. Cloning...")
            # Assuming clone.sh takes a directory as argument
            result = subprocess.run(["./shell/clone.sh", dir], cwd=script_dir)
            if result.returncode != 0:
                print(f"Failed to clone into {dir}")


def main():
    global script_dir

    # Check and clone any missing directories
    check_and_clone()

    subprocess.run(["./shell/build.sh"], cwd=script_dir)
    # Run company 2 containers by default
    subprocess.run(["./shell/runfrom.sh", "2", "2", "2", "2"], cwd=script_dir)

    help()

    while True:
        user_input = input("Enter a command: ")
        parse_input(user_input)


if __name__ == "__main__":
    main()
