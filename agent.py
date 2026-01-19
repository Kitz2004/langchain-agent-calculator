# agent.py
from dotenv import load_dotenv
load_dotenv()

import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# -----------------------------
# LLM (ONLY for intent detection)
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# TOOL AGENTS (PURE LOGIC)
# -----------------------------
@tool
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

@tool
def divide(a: float, b: float):
    """Divide two numbers"""
    if b == 0:
        return "Cannot divide by zero"
    return a / b

# -----------------------------
# INTENT DETECTION PROMPT
# -----------------------------
intent_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You extract math intent.\n"
        "Return ONLY valid JSON.\n"
        "Format:\n"
        "{ \"operation\": \"add|subtract|multiply|divide\", \"a\": number, \"b\": number }"
    ),
    ("human", "{input}")
])

# -----------------------------
# SAFE INTENT DETECTION
# -----------------------------
import re

def detect_intent(user_input: str):
    # ---------- RULE-BASED FIRST ----------
    numbers = list(map(float, re.findall(r"\d+\.?\d*", user_input.lower())))

    if len(numbers) == 2:
        a, b = numbers

        if "add" in user_input or "sum" in user_input or "plus" in user_input:
            return {"operation": "add", "a": a, "b": b}

        if "subtract" in user_input or "minus" in user_input:
            return {"operation": "subtract", "a": a, "b": b}

        if "multiply" in user_input or "times" in user_input:
            return {"operation": "multiply", "a": a, "b": b}

        if "divide" in user_input or "by" in user_input:
            return {"operation": "divide", "a": a, "b": b}

    # ---------- LLM FALLBACK ----------
    try:
        response = llm.invoke(
            intent_prompt.format_messages(input=user_input)
        )

        raw = response.content.strip()

        if not raw:
            return None

        # extract JSON safely
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not json_match:
            return None

        return json.loads(json_match.group())

    except Exception:
        return None


# -----------------------------
# CONTROLLED TOOL EXECUTION
# -----------------------------
def execute_agent(intent: dict):
    op = intent.get("operation")
    a = intent.get("a")
    b = intent.get("b")

    if op == "add":
        return add.invoke({"a": a, "b": b})
    elif op == "subtract":
        return subtract.invoke({"a": a, "b": b})
    elif op == "multiply":
        return multiply.invoke({"a": a, "b": b})
    elif op == "divide":
        return divide.invoke({"a": a, "b": b})
    else:
        return "Unsupported operation"
