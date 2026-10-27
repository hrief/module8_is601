"""Exercise real browser interactions and the live API together."""
from pathlib import Path
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.e2e

@pytest.mark.parametrize("button,a,b,result", [
    ("Add", "10", "5", "15"),
    ("Subtract", "-2.5", "3", "-5.5"),
    ("Multiply", "2.5", "4", "10"),
    ("Divide", "7", "2", "3.5"),
])
def test_calculator(page, fastapi_server, button, a, b, result):
    page.goto(fastapi_server)
    expect(page.locator("h1")).to_have_text("Hello World")
    page.fill("#a", a)
    page.fill("#b", b)
    page.get_by_role("button", name=button, exact=True).click()
    expect(page.locator("#result")).to_have_text(f"Calculation Result: {result}")
    if button == "Add":
        Path("screenshots").mkdir(exist_ok=True)
        page.screenshot(path="screenshots/application.png", full_page=True)

def test_error_and_recovery(page, fastapi_server):
    page.goto(fastapi_server)
    page.fill("#a", "10")
    page.fill("#b", "0")
    page.get_by_role("button", name="Divide", exact=True).click()
    expect(page.locator("#result")).to_have_text("Error: Cannot divide by zero!")
    page.fill("#b", "2")
    page.get_by_role("button", name="Divide", exact=True).click()
    expect(page.locator("#result")).to_have_text("Calculation Result: 5")

def test_empty_input(page, fastapi_server):
    page.goto(fastapi_server)
    page.get_by_role("button", name="Add", exact=True).click()
    expect(page.locator("#result")).to_contain_text("Error:")
