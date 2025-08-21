import json
import os

BUDGET_FILE = "budgets.json"

def load_budgets():
    """Load budgets from JSON file."""
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    return {"total": 1000.0, "categories": {}}  # defaults

def save_budgets(budgets):
    """Save budgets to JSON file."""
    with open(BUDGET_FILE, "w") as f:
        json.dump(budgets, f, indent=4)
