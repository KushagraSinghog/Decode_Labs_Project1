"""
memory.py

ConversationMemory — stores the full conversation history and exposes
helpers that the bot uses for context-aware replies and the __REPEAT__
special token.

Each turn is a MemoryEntry namedtuple:
    role      : "user" | "bot"
    text      : the raw text
    intent    : name of matched intent (None for user turns)
    timestamp : datetime of the turn
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, List, Optional


@dataclass
class MemoryEntry:
    role:      str                  # "user" | "bot"
    text:      str
    intent:    Optional[str] = None
    timestamp: datetime       = field(default_factory=datetime.now)

    def __str__(self) -> str:
        ts  = self.timestamp.strftime("%H:%M:%S")
        tag = f"[{self.intent}]" if self.intent else ""
        return f"[{ts}] {self.role.upper():>4} {tag}: {self.text}"


class ConversationMemory:
    """
    Maintains a bounded sliding-window of conversation turns.

    Parameters
    ----------
    max_turns : int
        Maximum number of entries kept in memory (default 100).
    """

    def __init__(self, max_turns: int = 100) -> None:
        self._history: Deque[MemoryEntry] = deque(maxlen=max_turns)
        self._context: Optional[str] = None          # current context tag
        self._intent_counts: dict[str, int] = {}     # intent frequency map

    # Write
    
    def add_user(self, text: str) -> None:
        """Record a user turn."""
        self._history.append(MemoryEntry(role="user", text=text))

    def add_bot(self, text: str, intent: str) -> None:
        """Record a bot turn and update intent frequency map."""
        self._history.append(MemoryEntry(role="bot", text=text, intent=intent))
        self._intent_counts[intent] = self._intent_counts.get(intent, 0) + 1

    # Context management
    
    @property
    def context(self) -> Optional[str]:
        return self._context

    @context.setter
    def context(self, value: Optional[str]) -> None:
        self._context = value

    # Read helpers
    
    def last_bot_response(self) -> Optional[str]:
        """Return the most recent bot response text, or None."""
        for entry in reversed(self._history):
            if entry.role == "bot":
                return entry.text
        return None

    def last_user_input(self) -> Optional[str]:
        """Return the most recent user input text, or None."""
        for entry in reversed(self._history):
            if entry.role == "user":
                return entry.text
        return None

    def recent_turns(self, n: int = 5) -> List[MemoryEntry]:
        """Return the last *n* turns."""
        return list(self._history)[-n:]

    def most_used_intent(self) -> Optional[str]:
        """Return the name of the most frequently matched intent."""
        if not self._intent_counts:
            return None
        return max(self._intent_counts, key=self._intent_counts.get)

    def summary(self) -> str:
        """Human-readable summary of the current session."""
        total_turns = len(self._history)
        user_turns  = sum(1 for e in self._history if e.role == "user")
        top_intent  = self.most_used_intent() or "N/A"
        return (
            f"Session summary → "
            f"Total turns: {total_turns}, "
            f"User messages: {user_turns}, "
            f"Top intent: {top_intent}, "
            f"Context: {self._context or 'general'}"
        )

    def full_history(self) -> List[MemoryEntry]:
        """Return the full history as a list."""
        return list(self._history)
