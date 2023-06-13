import argparse
import subprocess

def run(args):
    if not args.Company in ['1', '2']:
        print("Invalid company number provided")
        return 1
    cmd = f"./runfrom.sh {args.Company} {args.Company} {args.Company} {args.Company}"
    subprocess.run([cmd])

def run_from(args):
    for module in [args.Frontend, args.Backend, args.Algs1, args.Algs2]:
        if not module in ['1', '2']:
            print("Invalid company number provided")
            return 1
    cmd = f"./runfrom.sh {args.Frontend} {args.Backend} {args.Algs1} {args.Algs2}"
    subprocess.run([cmd])

def kill_all(args):
    subprocess.run(['killall.sh'])

def test(args):
    print("This has not been implemented yet")

def autotest_all(args):
    print("This has not been implemented yet")

def main():
    parser = argparse.ArgumentParser(description="CLI for running integration scripts")

    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser('run', help="Runs all four modules from a given company")
    run_parser.add_argument('Company', help="1 or 2")
    run_parser.set_defaults(func=run)

    run_parser = subparsers.add_parser('runfrom', help="Runs modules from each given company")
    run_parser.add_argument('Frontend', help="1 or 2")
    run_parser.add_argument('Backend', help="1 or 2")
    run_parser.add_argument('Algs1', help="1 or 2")
    run_parser.add_argument('Algs2', help="1 or 2")
    run_parser.set_defaults(func=run_from)

    subparsers.add_parser('stop', help="Terminate all running containers")
    run_parser.set_defaults(func=kill_all)

    subparsers.add_parser('test', help="Test the currently running containers")
    run_parser.set_defaults(func=test)

    subparsers.add_parser('testall', help="Run full test suite")
    run_parser.set_defaults(func=autotest_all)

if __name__ == "__main__":
    main()
