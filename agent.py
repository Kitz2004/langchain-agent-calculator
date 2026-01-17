from dotenv import load_dotenv
load_dotenv()

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

# ---------------- LLM ----------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# ---------------- AGENTS (TOOLS) ----------------

@tool
def add(expr: str) -> str:
    """Add two numbers given an expression like '4+5'."""
    a, b = map(float, expr.split("+"))
    return str(a + b)

@tool
def subtract(expr: str) -> str:
    """Subtract two numbers given an expression like '8-3'."""
    a, b = map(float, expr.split("-"))
    return str(a - b)

@tool
def multiply(expr: str) -> str:
    """Multiply two numbers given an expression like '6*7'."""
    a, b = map(float, expr.split("*"))
    return str(a * b)

@tool
def divide(expr: str) -> str:
    """Divide two numbers given an expression like '8/2'."""
    a, b = map(float, expr.split("/"))
    return str(a / b)

# ---------------- PROMPT ----------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract ONLY the math expression like 8/2, 4+5"),
    ("human", "{input}")
])

# ---------------- INTENT DETECTION ----------------
def detect_operation(user_input: str):
    expression = (prompt | llm).invoke({"input": user_input}).content.strip()

    if "+" in expression:
        return "ADD", expression
    if "-" in expression:
        return "SUBTRACT", expression
    if "*" in expression:
        return "MULTIPLY", expression
    if "/" in expression:
        return "DIVIDE", expression

    return None, None

# ---------------- EXECUTION ----------------
def execute_agent(operation: str, expression: str):
    if operation == "ADD":
        return add.invoke(expression)
    if operation == "SUBTRACT":
        return subtract.invoke(expression)
    if operation == "MULTIPLY":
        return multiply.invoke(expression)
    if operation == "DIVIDE":
        return divide.invoke(expression)
