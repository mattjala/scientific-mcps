"""
Test loader module for AI agent prompt tests.
Currently uses Claude Code CLI as the default agent, but designed to be agent-agnostic.
"""
import json
import yaml
import jsonschema
import subprocess
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestResult:
    """Result of a single test execution."""
    name: str
    passed: bool
    error_message: str = ""
    response: str = ""
    execution_time: float = 0.0


class AIAgentTestLoader:
    """Loads and executes AI agent prompt tests from YAML files.
    Currently uses Claude Code CLI but designed to support multiple AI agents."""

    def __init__(self, yaml_file: str):
        """Initialize the test loader.
        
        Args:
            yaml_file: Path to the YAML test file
        """
        self.yaml_file = yaml_file
        self.tests = self._load_tests()

    def _load_tests(self) -> List[Dict[str, Any]]:
        """Load tests from YAML file."""
        with open(self.yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        return data.get('tests', [])

    def _call_ai_agent(self, prompt: str, timeout: int = 30) -> str:
        """Call AI agent with the given prompt.
        Currently uses Claude Code CLI, but this method can be extended for other agents."""
        cmd = ["claude", "--print", "--output-format", "json", prompt]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )
            
            # Parse the JSON response from the AI agent
            response_data = json.loads(result.stdout)
            
            # Extract the actual text content from the response
            # Claude Code CLI returns structured data, we want the result
            if isinstance(response_data, dict) and 'result' in response_data:
                return response_data['result']
            elif isinstance(response_data, str):
                return response_data
            else:
                return str(response_data)

        except subprocess.TimeoutExpired:
            raise Exception(f"AI agent timed out after {timeout} seconds")
        except subprocess.CalledProcessError as e:
            raise Exception(f"AI agent failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI agent output as JSON: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error calling AI agent: {e}")

    def _validate_json_response(self, response: str, expected_schema: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate JSON response against schema.

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Extract JSON from markdown code block if present
            json_content = response.strip()
            if json_content.startswith('```json'):
                # Find the JSON content between ```json and ```
                start_idx = json_content.find('```json') + 7
                end_idx = json_content.find('```', start_idx)
                if end_idx != -1:
                    json_content = json_content[start_idx:end_idx].strip()
            elif json_content.startswith('```'):
                # Handle generic code blocks
                start_idx = json_content.find('```') + 3
                end_idx = json_content.find('```', start_idx)
                if end_idx != -1:
                    json_content = json_content[start_idx:end_idx].strip()
            
            # Parse JSON
            data = json.loads(json_content)
            
            # Validate against schema
            jsonschema.validate(data, expected_schema)

            return True, ""
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except jsonschema.ValidationError as e:
            return False, f"Schema validation failed: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def run_test(self, test_config: Dict[str, Any]) -> TestResult:
        """Run a single test."""
        start_time = datetime.now()

        try:
            # Get test parameters
            name = test_config['name']
            prompt = test_config['prompt']
            expected_schema = test_config['expected_schema']
            timeout = test_config.get('timeout', 30)

            # Call AI agent
            response = self._call_ai_agent(prompt, timeout)

            # Validate response
            is_valid, error_msg = self._validate_json_response(response, expected_schema)

            execution_time = (datetime.now() - start_time).total_seconds()

            return TestResult(
                name=name,
                passed=is_valid,
                error_message=error_msg,
                response=response,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TestResult(
                name=test_config.get('name', 'unknown'),
                passed=False,
                error_message=f"Test execution failed: {str(e)}",
                response="",
                execution_time=execution_time
            )

    def run_all_tests(self) -> List[TestResult]:
        """Run all tests and return results."""
        results = []

        for test_config in self.tests:
            result = self.run_test(test_config)
            results.append(result)

        return results

    def print_results(self, results: List[TestResult]) -> None:
        """Print test results in a readable format."""
        print(f"\n{'='*60}")
        print(f"AI Agent Prompt Test Results")
        print(f"{'='*60}")

        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.passed)
        failed_tests = total_tests - passed_tests

        for result in results:
            status = "PASS" if result.passed else "FAIL"
            print(f"\n{result.name}: {status} ({result.execution_time:.2f}s)")

            if not result.passed:
                print(f"  Error: {result.error_message}")

            if result.response:
                print(f"  Response: {result.response[:100]}...")

        print(f"\n{'='*60}")
        print(f"Total: {total_tests} | Passed: {passed_tests} | Failed: {failed_tests}")
        print(f"{'='*60}")

        return failed_tests == 0