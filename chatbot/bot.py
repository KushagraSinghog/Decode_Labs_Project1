"""
bot.py

Central chatbot orchestrator class.

Responsibilities
----------------
- Owns an IntentMatcher, ConversationMemory, and logger instance.
- Calls matcher.match() on every user turn.
- Resolves special response tokens (__TIME__, __DATE__, __MATH__, __REPEAT__).
- Picks a random response from the matched intent's list.
- Updates memory and context after each turn.
- Exposes a single respond(text) → str public method.
"""

from __future__ import annotations

import math
import random
import re
from datetime import datetime
from typing import Optional

from .intents  import Intent
from .logger   import get_logger
from .matcher  import IntentMatcher
from .memory   import ConversationMemory

log = get_logger(__name__)


class Chatbot:
    """
    Rule-based chatbot with OOP design, intent matching,
    conversation memory, and structured logging.

    Parameters:
    
        name       : Display name for the bot (default "Nexus").
        max_memory : Maximum turns kept in conversation memory.
    """

    def __init__(self, name: str = "Nexus", max_memory: int = 100) -> None:
        self.name    = name
        self._matcher = IntentMatcher()
        self._memory  = ConversationMemory(max_turns=max_memory)
        log.info("Chatbot '%s' initialised.", self.name)

    # Public API

    def respond(self, user_text: str) -> str:
        """
        Process *user_text* and return a reply string.

        Flow:
        
            1. Record user turn in memory.
            2. Match intent (context-aware).
            3. Pick a response template.
            4. Resolve any special tokens.
            5. Record bot turn in memory.
            6. Update context.
            7. Return final reply.
        """
        user_text = user_text.strip()
        if not user_text:
            return "Seems like you didn't type anything! Try again. 😊"

        log.debug("User said: %r", user_text)
        self._memory.add_user(user_text)

        # Intent matching 
        intent, confidence = self._matcher.match(user_text, self._memory.context)
        log.info(
            "Intent matched: %-20s | confidence: %.2f | context: %s",
            intent.name, confidence, self._memory.context or "none",
        )

        # Pick response template 
        template = random.choice(intent.responses)

        # Resolve special tokens 
        reply = self._resolve_token(template, user_text)

        # Update memory & context 
        self._memory.add_bot(reply, intent.name)
        if intent.context:
            self._memory.context = intent.context
            log.debug("Context updated to: %s", intent.context)

        log.debug("Bot replied: %r", reply)
        return reply

    @property
    def is_exit_requested(self) -> bool:
        """True if the last matched intent set the 'exit' context."""
        return self._memory.context == "exit"

    def session_summary(self) -> str:
        """Return a one-line session summary from memory."""
        return self._memory.summary()

    def history(self, n: int = 10):
        """Return the last *n* conversation entries."""
        return self._memory.recent_turns(n)

    # Special token resolver
    
    def _resolve_token(self, template: str, user_text: str) -> str:
        """Swap special __TOKEN__ placeholders with dynamic content."""

        if template == "__TIME__":
            now = datetime.now().strftime("%I:%M %p")
            return f"🕐 The current time is {now}."

        if template == "__DATE__":
            today = datetime.now().strftime("%A, %d %B %Y")
            return f"📅 Today is {today}."

        if template == "__REPEAT__":
            last = self._memory.last_bot_response()
            return f'I said: \u201c{last}\u201d' if last else "I haven't said anything yet!"

        if template == "__MATH__":
            return self._handle_math(user_text)

        return template

    # Math mini-evaluator
    
    @staticmethod
    def _handle_math(text: str) -> str:
        """
        Extract simple arithmetic from user text and evaluate it.
        Supports: +, -, *, /, ^  and keywords (plus, minus, times, divided).
        """
        # Translate keywords
        expr = text.lower()
        expr = re.sub(r"\bplus\b",        "+", expr)
        expr = re.sub(r"\bminus\b",       "-", expr)
        expr = re.sub(r"\btimes\b",       "*", expr)
        expr = re.sub(r"\bdivided by\b",  "/", expr)
        expr = re.sub(r"\bto the power of\b", "**", expr)

        # Extract the numeric expression
        match = re.search(r"[\d\s\+\-\*\/\.\(\)\^]+", expr)
        if not match:
            return "Could you write that as a math expression? e.g. '12 + 7' or '15 times 3'."

        raw = match.group(0).strip().replace("^", "**")
        try:
            # Safe eval: only allow numbers and operators
            allowed = set("0123456789 +-*/().**")
            if not all(c in allowed for c in raw):
                raise ValueError("Unsafe characters detected.")
            result = eval(raw, {"__builtins__": {}}, {"math": math})  # noqa: S307
            return f"🧮 {raw.strip()} = **{result}**"
        except ZeroDivisionError:
            return "⚠️ Division by zero? Even I can't handle that!"
        except Exception:
            return "Hmm, I couldn't work that out. Try something like '12 + 7'."
