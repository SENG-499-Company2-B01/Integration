import unittest
from unittest import mock
from io import StringIO
import sys
import os

# Import the functions to be tested
from integration import (
    load_config,
    build_service,
    kill_service,
    run_service,
    swap_service,
    create_company_dir,
    clone_repo,
    clone_company
)

class TestYourScript(unittest.TestCase):

    def test_load_config(self):
        # Define a temporary config file
        config = {
            "company1": {
                "frontend": {
                    "build": "build_frontend_command",
                    "run": "run_frontend_command"
                }
            },
            "company2": {
                "backend": {
                    "build": "build_backend_command",
                    "run": "run_backend_command"
                }
            }
        }
        with open('temp_config.json', 'w') as f:
            json.dump(config, f)

        # Test loading the temporary config file
        expected_config = {
            "company1": {
                "frontend": {
                    "build": "build_frontend_command",
                    "run": "run_frontend_command"
                }
            },
            "company2": {
                "backend": {
                    "build": "build_backend_command",
                    "run": "run_backend_command"
                }
            }
        }
        self.assertEqual(load_config(), expected_config)

        # Clean up the temporary config file
        os.remove('temp_config.json')

    def test_build_service(self):
        # Mock the subprocess.run function
        with mock.patch('subprocess.run') as mock_run:
            build_service('company1', 'frontend')
            mock_run.assert_called_once_with('build_frontend_command', cwd='/path/to/company1/frontend', shell=True, check=True)

    def test_kill_service(self):
        # Mock the subprocess.run function
        with mock.patch('subprocess.run') as mock_run:
            kill_service('frontend')
            mock_run.assert_called_once_with(['docker', 'container', 'stop', 'frontend_2'], cwd='/path/to/script_dir', check=True)

    # Write similar test cases for other functions...

if __name__ == '__main__':
    unittest.main()
