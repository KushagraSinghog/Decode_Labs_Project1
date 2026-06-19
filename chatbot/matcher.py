"""
matcher.py

IntentMatcher — converts raw user text into a matched Intent.

Matching pipeline:
    1. Normalise    → lowercase, strip punctuation
    2. Tokenise     → split into words
    3. Keyword scan → check each pattern word/phrase against tokens
    4. Score        → count pattern hits; pick highest scoring intent
    5. Threshold    → if score == 0, return fallback intent
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from .intents import Intent, INTENTS


class IntentMatcher:
    """
    Matches a user's raw input string to the best-fit Intent.

    Attributes:
    
        intents : List[Intent]
            All registered intents (excluding fallback which is stored separately).
        fallback : Intent
            Returned when no patterns match.
    """

    def __init__(self, intents: List[Intent] = INTENTS) -> None:
        self._fallback = next(i for i in intents if i.name == "fallback")
        self._intents  = [i for i in intents if i.name != "fallback"]

    # Public API
    
    def match(self, text: str, context: Optional[str] = None) -> Tuple[Intent, float]:
        """
        Match *text* against all intents and return (best_intent, confidence).

        Parameters:
        
            text    : raw user input
            context : current conversation context tag (may restrict intents)

        Returns:
        
            (Intent, confidence_score 0.0-1.0)
        """
        normalised = self._normalise(text)
        tokens     = normalised.split()

        best_intent: Intent = self._fallback
        best_score:  float  = 0.0

        for intent in self._intents:
            # Context gate: skip intents that require a specific context
            if intent.requires_context and intent.requires_context != context:
                continue

            score = self._score(normalised, tokens, intent)
            if score > best_score:
                best_score  = score
                best_intent = intent

        # Normalise score to [0, 1]
        confidence = min(best_score, 1.0)
        return best_intent, confidence

    # Private helpers
    
    @staticmethod
    def _normalise(text: str) -> str:
        """Lowercase and remove most punctuation."""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)    # replace punctuation with space
        text = re.sub(r"\s+", " ", text)        # collapse whitespace
        return text

    @staticmethod
    def _score(normalised: str, tokens: List[str], intent: Intent) -> float:
        """
        Score an intent by taking the maximum score among its patterns.

        Scoring rules:
        - Whole phrase matched with word boundaries -> 1.0
        - Token matching -> +0.6 per exact token, +0.2 for starts-with.
          Total tokens score is capped at 0.9.
        """
        max_pattern_score = 0.0

        for pattern in intent.patterns:
            p_norm = re.sub(r"[^\w\s]", " ", pattern.lower()).strip()
            if not p_norm:
                continue

            # Exact phrase check with word boundaries
            pattern_regex = r"\b" + re.escape(p_norm) + r"\b"
            if re.search(pattern_regex, normalised):
                pattern_score = 1.0
            else:
                # Token-by-token scoring
                token_hits = 0.0
                p_tokens = p_norm.split()
                for pt in p_tokens:
                    if pt in tokens:
                        token_hits += 0.6
                    elif any(t.startswith(pt) for t in tokens):
                        token_hits += 0.2
                pattern_score = min(token_hits, 0.9)

            if pattern_score > max_pattern_score:
                max_pattern_score = pattern_score

        return max_pattern_score
