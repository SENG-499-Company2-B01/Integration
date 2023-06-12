# Integration
Integration scripts and tests maintained by algs2

## How it works

First build the image with `docker-compose build`.

This will clone all of the repositories, and build the docker images for each repository.

Then, start the container with `docker-compose up`.

This will start the company 2 containers on your host machine.

More features coming soon...

## Testing

### Selenium
Selenium Webdriver is used to test the integration between our backend and the UI. Individual test cases can be found in the `/test/test_cases` directory, and they reference selenium page objects in `/test/page.py`.

Any selenium element locators should be contained within the `locators.py` file and accessed via the page objects, not directly from the test cases in order to ensure easily readable tests.
