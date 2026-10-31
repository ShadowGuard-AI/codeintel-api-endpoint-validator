import argparse
import logging
import os
import sys
import yaml
import json
from typing import List, Dict
from urllib.parse import urlparse
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class APIEndpointValidator:
    """
    Validates API endpoints against a defined schema.
    """

    def __init__(self, code_path: str, schema_path: str):
        """
        Initializes the APIEndpointValidator.

        Args:
            code_path: Path to the codebase.
            schema_path: Path to the API schema (OpenAPI/Swagger).
        """
        self.code_path = code_path
        self.schema_path = schema_path
        self.endpoints = []
        self.schema = None
        self.files_scanned = 0

    def load_schema(self) -> None:
        """
        Loads the API schema from the specified file. Supports YAML and JSON.
        """
        try:
            with open(self.schema_path, 'r') as f:
                if self.schema_path.endswith('.yaml') or self.schema_path.endswith('.yml'):
                    self.schema = yaml.safe_load(f)
                elif self.schema_path.endswith('.json'):
                    self.schema = json.load(f)
                else:
                    raise ValueError("Unsupported schema file format. Only YAML and JSON are supported.")
        except FileNotFoundError:
            logging.error(f"Schema file not found: {self.schema_path}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML schema: {e}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON schema: {e}")
            raise
        except Exception as e:
            logging.error(f"Error loading schema: {e}")
            raise

        # An empty YAML file loads as None. Leaving self.schema as None
        # made validate_endpoints report "Schema not loaded", which
        # sends the reader hunting for a missing load_schema call when
        # the actual problem is an empty or malformed schema file.
        if not isinstance(self.schema, dict):
            raise ValueError(
                f"Schema file must contain a mapping at the top level, got {type(self.schema).__name__}."
            )

    def find_endpoints(self) -> None:
        """
        Finds potential API endpoints in the codebase.
        This is a basic implementation and can be expanded with more sophisticated parsing.
        """
        if not os.path.exists(self.code_path):
            raise FileNotFoundError(f"Code path does not exist: {self.code_path}")
        try:
            for root, _, files in os.walk(self.code_path):
                for file in files:
                    if file.endswith('.py'):
                        self.files_scanned += 1
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            content = f.read()
                            # Decorator forms on app, blueprint, router,
                            # and similar objects: route, get, post, put,
                            # delete, and patch.
                            matches = re.findall(
                                r"@\w+\.(?:route|get|post|put|delete|patch)\(['\"](.*?)['\"]",
                                content)
                            self.endpoints.extend([(file_path, endpoint) for endpoint in matches])
            logging.info(
                f"Scanned {self.files_scanned} Python file(s), "
                f"found {len(self.endpoints)} endpoint(s) to check.")
        except Exception as e:
            logging.error(f"Error finding endpoints: {e}")
            raise

    def validate_endpoints(self) -> List[str]:
        """
        Validates the found endpoints against the schema.

        Returns:
            A list of validation errors.
        """
        if not self.schema:
            logging.error("Schema not loaded. Call load_schema() first.")
            return ["Schema not loaded."]

        errors = []
        if 'paths' not in self.schema:
            logging.warning("No 'paths' defined in the schema.  Cannot validate endpoints.")
            return ["No paths defined in schema"]

        # Membership tests and key lookups below assume paths maps path
        # strings to per-path objects. A schema whose paths is a list
        # used to die inside the loop with a list indices error that
        # named neither the schema nor the real problem.
        if not isinstance(self.schema['paths'], dict):
            return [f"Schema 'paths' must be a mapping, got {type(self.schema['paths']).__name__}"]

        for file_path, endpoint in self.endpoints:
            if endpoint not in self.schema['paths']:
                errors.append(f"Endpoint '{endpoint}' (defined in {file_path}) not found in schema.")
            else:
                logging.debug(f"Endpoint '{endpoint}' found in schema.")

                # Example validation: Check if the schema defines allowed methods (GET, POST, etc.)
                methods = self.schema['paths'][endpoint].keys()
                if not any(method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head'] for method in methods):
                    errors.append(f"Endpoint '{endpoint}' in schema does not define valid HTTP methods.")

        return errors


def setup_argparse() -> argparse.ArgumentParser:
    """
    Sets up the argument parser for the CLI.

    Returns:
        An argparse.ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(description="Scans codebase for API endpoints and validates them against a schema.")
    parser.add_argument("code_path", help="Path to the codebase to scan.")
    parser.add_argument("schema_path", help="Path to the API schema file (OpenAPI/Swagger).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")

    return parser


def main() -> None:
    """
    Main function to run the API endpoint validator.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose logging enabled.")

    if not os.path.exists(args.code_path):
        logging.error(f"Code path does not exist: {args.code_path}")
        sys.exit(1)

    try:
        validator = APIEndpointValidator(args.code_path, args.schema_path)
        validator.load_schema()
        validator.find_endpoints()
        errors = validator.validate_endpoints()
        logging.info(
            f"Checked {len(validator.endpoints)} endpoint(s) "
            f"from {validator.files_scanned} scanned file(s).")

        if errors:
            logging.error("API Endpoint Validation Failed:")
            for error in errors:
                logging.error(error)
            sys.exit(1)
        else:
            logging.info("API Endpoint Validation Passed.")

    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Example usage:
    # python main.py ./example_code ./example_schema.yaml
    #
    # Example codebase structure (./example_code):
    # - app.py (contains @app.route('/users') and @app.route('/items/{item_id}')
    #
    # Example schema (./example_schema.yaml):
    # paths:
    #   /users:
    #     get:
    #       summary: Get all users
    #   /items/{item_id}:
    #     get:
    #       summary: Get a specific item
    main()