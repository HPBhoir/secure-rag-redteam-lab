def calculator(expression: str):
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return {"tool": "calculator", "result": result}
    except Exception as e:
        return {"tool": "calculator", "error": str(e)}


def mock_sensitive_api():
    return {
        "tool": "mock_sensitive_api",
        "employees": [
            {"name": "Alice", "role": "Manager", "salary": "95000"},
            {"name": "Bob", "role": "Engineer", "salary": "87000"},
        ],
        "incident_status": "Internal review in progress",
        "finance_summary": {
            "quarter": "Q4",
            "revenue": "$1.2M",
            "margin": "18%"
        }
    }
