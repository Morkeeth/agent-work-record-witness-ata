#!/usr/bin/env python3
"""Fleet supervisor — ADK wraps plain propagation functions.

build_agent() must succeed on the stripped judge path: default model id is set
when GEMINI_MODEL is unset (eligibility strips env). Tools still work without ADK.
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fleet.propagate import find_best_prompt, propagate_prompt, witness_propagation  # noqa: E402

# Verified live on this machine; free-tier ladder starts here.
DEFAULT_MODEL = "gemini-2.5-flash-lite"

INSTRUCTION = """You are the fleet supervisor for org prompt propagation.

When asked to propagate the best operator prompt for a task:
1. Call find_best_prompt with the topic and corpus paths.
2. Call propagate_prompt with the returned prompt_text.
3. Call witness_propagation on the target skill path.

Never assert a prompt landed without calling witness_propagation.
If find_best_prompt returns an error, say so — do not invent a prompt.
"""


def find_best_prompt_tool(topic: str, corpus_glob: str = "fixtures/operators/*.jsonl") -> dict:
    """Find the best human prompt on a task class across operator transcripts."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = glob.glob(os.path.join(root, corpus_glob))
    return find_best_prompt(topic, paths)


def propagate_prompt_tool(prompt_text: str, target_skill_path: str,
                          operator: str = "unknown", topic: str = "") -> dict:
    """Write curated prompt text to an org skill file (never executes transcript text)."""
    return propagate_prompt(prompt_text, target_skill_path, operator=operator, topic=topic)


def witness_propagation_tool(target_skill_path: str) -> dict:
    """Ground truth: did the propagated skill file land on disk?"""
    return witness_propagation(target_skill_path)


TOOLS = [find_best_prompt_tool, propagate_prompt_tool, witness_propagation_tool]


def build_agent():
    model = os.environ.get("GEMINI_MODEL") or DEFAULT_MODEL
    try:
        from google.adk.agents import Agent
    except ImportError as e:
        raise RuntimeError("pip install google-adk — tools work without it") from e
    return Agent(
        name="fleet_supervisor",
        model=model,
        description="Finds the org's best operator prompt and propagates it to the team skill file.",
        instruction=INSTRUCTION,
        tools=TOOLS,
    )
