from crewai.tools import tool


@tool("Calculator")
def calculator(expression: str) -> str:
    """
    Calculate a basic mathematical expression.

    Example:
    25 * 4
    100 / 5
    12 + 8
    """

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result is {result}"

    except Exception:
        return "I could not calculate that expression."
