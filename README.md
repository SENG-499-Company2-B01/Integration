# Integration
Integration scripts and tests maintained by algs2

## Running company 2 application

### Dependancies

- Docker

### Build

First build the image with `docker-compose build`.

This will clone all of the repositories and build the docker image.

### Run

Then, start the container with `docker-compose up`.

This will build and start the company 2 containers on your host machine.

## Full features

TO access the full features of this repository, some additional setup is required.

### Dependancies

- Docker
- Python3

Run `pip install -r requirements.txt` to install the required python packages.

### Run

To run the full features, run `python3 integration.py`.

### Commands

- `help` - This function prints a list of available commands, their syntax, and a brief description of their function.

- `run [Company]` - This command runs all four modules from a given company. Replace [Company] with either 1 or 2 to specify the company.

- `runfrom [Frontend] [Backend] [Algs1] [Algs2]` - This command runs modules from each given company. For each module ([Frontend], [Backend], [Algs1], [Algs2]), replace the placeholder with 1 or 2 to indicate which company's module to run from.

- `exit` - This command terminates all running containers and exits the program.

- `test` - This command tests the currently running containers. Note: This feature has not been implemented yet.

- `testall` - This command runs a full test suite. Note: This feature has not been implemented yet.

### Selenium
Selenium Webdriver is used to test the integration between our backend and the UI. Individual test cases can be found in the `/test/test_cases` directory, and they reference selenium page objects in `/test/page.py`.

Any selenium element locators should be contained within the `locators.py` file and accessed via the page objects, not directly from the test cases in order to ensure easily readable tests.
