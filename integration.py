import subprocess

def help():
    print("""
    Available commands:
    1. run [Company] - Runs all four modules from a given company. Provide 1 or 2 for the company.
    2. runfrom [Frontend] [Backend] [Algs1] [Algs2] - Runs modules from each given company. For each module, provide 1 or 2 to indicate which company to run from.
    3. exit - Terminate all running containers and exit the program.
    4. test - Test the currently running containers. This has not been implemented yet.
    5. testall - Run full test suite. This has not been implemented yet.
    """)

def run(company):
    if not company in ['1', '2']:
        print("Invalid company number provided")
        return 1
    subprocess.run(["./shell/runfrom.sh", company, company, company, company], cwd="/app")

def run_from(frontend_company, backend_company, algs1_company, algs2_company):
    for module in [frontend_company, backend_company, algs1_company, algs2_company]:
        if not module in ['1', '2']:
            print("Invalid company number provided")
            return 1
    subprocess.run(["./shell/runfrom.sh", frontend_company, backend_company, algs1_company, algs2_company], cwd="/app")

def kill_all():
    subprocess.run(['./shell/killall.sh'], cwd="/app")

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
    elif command == 'exit':
        kill_all()
        exit(0)
    elif command == 'test':
        test()
    elif command == 'testall':
        autotest_all()
    else:
        help()

def main():
     # Run company 2 containers by default
    subprocess.run(["./shell/runfrom.sh", "2", "2", "2", "2"], cwd="/app")

    help()

    while True:
        user_input = input("Enter a command: ")
        parse_input(user_input)

if __name__ == "__main__":
    main()
