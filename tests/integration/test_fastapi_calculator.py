# tests/integration/test_fastapi_calculator.py

import pytest  # Import the pytest framework for writing and running tests
from fastapi.testclient import TestClient  # Import TestClient for simulating API requests
from main import app  # Import the FastAPI app instance from your main application file

# ---------------------------------------------
# Pytest Fixture: client
# ---------------------------------------------

@pytest.fixture
def client():
    """
    Pytest Fixture to create a TestClient for the FastAPI application.

    This fixture initializes a TestClient instance that can be used to simulate
    requests to the FastAPI application without running a live server. The client
    is yielded to the test functions and properly closed after the tests complete.

    Benefits:
    - Speeds up testing by avoiding the overhead of running a server.
    - Allows for testing API endpoints in isolation.
    """
    with TestClient(app) as client:
        yield client  # Provide the TestClient instance to the test functions

# ---------------------------------------------
# Test Function: test_add_api
# ---------------------------------------------

def test_add_api(client):
    """
    Test the Addition API Endpoint.

    This test verifies that the `/add` endpoint correctly adds two numbers provided
    in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/add` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`15`).
    """
    # Send a POST request to the '/add' endpoint with JSON payload
    response = client.post('/add', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 15, f"Expected result 15, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_subtract_api
# ---------------------------------------------

def test_subtract_api(client):
    """
    Test the Subtraction API Endpoint.

    This test verifies that the `/subtract` endpoint correctly subtracts the second number
    from the first number provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/subtract` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`5`).
    """
    # Send a POST request to the '/subtract' endpoint with JSON payload
    response = client.post('/subtract', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 5, f"Expected result 5, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_multiply_api
# ---------------------------------------------

def test_multiply_api(client):
    """
    Test the Multiplication API Endpoint.

    This test verifies that the `/multiply` endpoint correctly multiplies two numbers
    provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/multiply` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`50`).
    """
    # Send a POST request to the '/multiply' endpoint with JSON payload
    response = client.post('/multiply', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 50, f"Expected result 50, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_divide_api
# ---------------------------------------------

def test_divide_api(client):
    """
    Test the Division API Endpoint.

    This test verifies that the `/divide` endpoint correctly divides the first number
    by the second number provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data `{'a': 10, 'b': 2}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`5`).
    """
    # Send a POST request to the '/divide' endpoint with JSON payload
    response = client.post('/divide', json={'a': 10, 'b': 2})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 5, f"Expected result 5, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_divide_by_zero_api
# ---------------------------------------------

def test_divide_by_zero_api(client):
    """
    Test the Division by Zero API Endpoint.

    This test verifies that the `/divide` endpoint correctly handles division by zero
    by returning an appropriate error message and status code.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data `{'a': 10, 'b': 0}`.
    2. Assert that the response status code is `400 Bad Request`.
    3. Assert that the JSON response contains an 'error' field with the message "Cannot divide by zero!".
    """
    # Send a POST request to the '/divide' endpoint with JSON payload attempting division by zero
    response = client.post('/divide', json={'a': 10, 'b': 0})
    
    # Assert that the response status code is 400 (Bad Request), indicating an error occurred
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    
    # Assert that the JSON response contains an 'error' field
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"
    
    # Assert that the 'error' field contains the correct error message
    assert "Cannot divide by zero!" in response.json()['error'], \
        f"Expected error message 'Cannot divide by zero!', got '{response.json()['error']}'"


@pytest.mark.parametrize("endpoint", ["add", "subtract", "multiply", "divide"])
@pytest.mark.parametrize("payload", [{}, {"a": 1}, {"a": "bad", "b": 2}, {"a": None, "b": 2}, {"a": True, "b": 2}, {"a": "NaN", "b": 2}])
def test_invalid_requests(client, endpoint, payload):
    response = client.post(f"/{endpoint}", json=payload)
    assert response.status_code == 400
    assert response.json()["error"]


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Calculator" in response.text


@pytest.mark.parametrize("endpoint", ["add", "subtract", "multiply", "divide"])
def test_internal_failure(client, monkeypatch, endpoint, caplog):
    def fail(*args):
        raise RuntimeError("private implementation detail")
    monkeypatch.setattr(f"main.{endpoint}", fail)
    response = client.post(f"/{endpoint}", json={"a": 10, "b": 2})
    assert response.status_code == 500
    assert response.json() == {"error": "Internal Server Error"}
    assert "private implementation detail" in caplog.text


@pytest.mark.parametrize("endpoint,a,b", [("add", 1e308, 1e308), ("subtract", -1e308, 1e308), ("multiply", 1e308, 2), ("divide", 1e308, 1e-308)])
def test_overflow(client, endpoint, a, b):
    response = client.post(f"/{endpoint}", json={"a": a, "b": b})
    assert response.status_code == 400
    assert response.json() == {"error": "Result must be a finite number."}


def test_malformed_json(client):
    response = client.post("/add", content="{", headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert "error" in response.json()


def test_logs_success_and_validation(client, caplog):
    client.post("/add", json={"a": 2, "b": 3})
    client.post("/add", json={})
    assert "add(2.0, 3.0) = 5.0" in caplog.text
    assert "ValidationError on /add" in caplog.text
