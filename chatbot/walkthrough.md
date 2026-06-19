# Chatbot Implementation Walkthrough

A modular, Object-Oriented Programming (OOP) rule-based Python chatbot named **Nexus** has been successfully implemented in the workspace.

## Highlights of Implementation

### 1. Modular Architecture
The chatbot code is fully modular, adhering to clean OOP principles:
- [__init__.py](file:///d:/Honey/DecodeLabs/chatbot/__init__.py): Exposes the primary public interface.
- [bot.py](file:///d:/Honey/DecodeLabs/chatbot/bot.py): Contains the core `Chatbot` orchestrator class.
- [intents.py](file:///d:/Honey/DecodeLabs/chatbot/intents.py): Holds defined structured `Intent` dataclasses and the registry.
- [matcher.py](file:///d:/Honey/DecodeLabs/chatbot/matcher.py): Implements a robust `IntentMatcher` supporting full phrase searches (word-boundary gated) and token-by-token scoring.
- [memory.py](file:///d:/Honey/DecodeLabs/chatbot/memory.py): Manages sliding window conversation logs, frequency tracking, and context.
- [logger.py](file:///d:/Honey/DecodeLabs/chatbot/logger.py): Configures a console/file logging system (UTF-8 safe for Windows).
- [main.py](file:///d:/Honey/DecodeLabs/main.py): Entry script running a continuous interactive CLI loop.

### 2. Decision Logic and Intent Matching
- Employs an if-else token resolution system for dynamic outputs (e.g. `__TIME__`, `__DATE__`, `__REPEAT__`, and `__MATH__`).
- Utilizes pattern matching regex with word boundaries `\b` to avoid false positives (e.g., matching the short intent token `ty` within words like `party`).
- Scoring takes the maximum score among patterns rather than summing them, preventing score inflation.

---

## Verification & Testing

### Automated Test Suite
A unit test suite has been added at [test_chatbot.py](file:///d:/Honey/DecodeLabs/test_chatbot.py) to cover:
- Core matching capabilities (Greetings, Farewell, Math, Fallbacks)
- Conversation history limit and sliding-window logic
- Dynamic math parsing and boundary conditions (e.g., division by zero)
- Conversation recall (`repeat`)

### Test Results
Run command: `python -m unittest test_chatbot.py`
All 9 unit tests passed successfully:
```text
12:04:33  INFO      chatbot :: Logger initialised - writing to D:\Honey\DecodeLabs\logs\chatbot.log
12:04:33  INFO      chatbot.chatbot.bot :: Chatbot 'TestNexus' initialised.
12:04:33  INFO      chatbot.chatbot.bot :: Intent matched: math                 | confidence: 1.00 | context: none
.........
----------------------------------------------------------------------
Ran 9 tests in 0.007s

OK
```
