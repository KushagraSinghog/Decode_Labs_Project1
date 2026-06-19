"""
intents.py

Defines all bot intents as structured dataclasses.
Each intent carries:
  - name       : unique identifier
  - patterns   : list of trigger keyword/phrase patterns
  - responses  : list of possible replies (picked randomly)
  - context    : optional context tag set after this intent fires
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class Intent:
    name: str
    patterns: List[str]
    responses: List[str]
    context: Optional[str] = None   # context tag this intent sets
    requires_context: Optional[str] = None  # fires only in this context


# Intent Registry

INTENTS: List[Intent] = [

    # Greetings 
    Intent(
        name="greeting",
        patterns=["hello", "hi", "hey", "howdy", "greetings", "sup", "what's up"],
        responses=[
            "Hey there! 👋 How can I help you today?",
            "Hello! Great to see you. What's on your mind?",
            "Hi! I'm your friendly chatbot. Ask me anything!",
        ],
        context="general",
    ),

    # Farewell / Exit 
    Intent(
        name="farewell",
        patterns=["bye", "goodbye", "quit", "exit", "see you", "later", "cya", "farewell"],
        responses=[
            "Goodbye! It was lovely chatting with you. 👋",
            "See you later! Take care! 😊",
            "Bye! Come back anytime you need help. ✨",
        ],
        context="exit",  # signals the loop to stop
    ),

    # How are you 
    Intent(
        name="how_are_you",
        patterns=["how are you", "how r u", "how do you do", "you ok", "are you okay", "how's it going"],
        responses=[
            "I'm doing great, thanks for asking! 😄 How about you?",
            "Feeling fantastic! I love talking to people. How are you doing?",
            "I'm always happy when I'm chatting! What's up?",
        ],
    ),

    # Name inquiry 
    Intent(
        name="bot_name",
        patterns=["your name", "who are you", "what are you", "what's your name", "call you"],
        responses=[
            "I'm Nexus 🤖 — your rule-based AI companion!",
            "They call me Nexus. Nice to meet you!",
            "I go by Nexus. What can I do for you today?",
        ],
    ),

    # Capabilities 
    Intent(
        name="capabilities",
        patterns=["what can you do", "help", "capabilities", "features", "what do you know"],
        responses=[
            (
                "I can chat about:\n"
                "  • Greetings & small talk\n"
                "  • Jokes & fun facts\n"
                "  • Time & date\n"
                "  • Weather (placeholder)\n"
                "  • Motivational quotes\n"
                "  • Math (add/sub/mul)\n"
                "Just type naturally!"
            ),
        ],
    ),

    # Jokes 
    Intent(
        name="joke",
        patterns=["joke", "tell me a joke", "make me laugh", "funny", "humor"],
        responses=[
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads. 🍫",
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "I asked my dog what 2 minus 2 is. He said nothing. 🐶",
        ],
    ),

    # Fun Facts 
    Intent(
        name="fun_fact",
        patterns=["fun fact", "tell me something", "interesting fact", "did you know", "fact"],
        responses=[
            "🧠 Fact: Honey never spoils — archaeologists have found 3000-year-old honey in Egyptian tombs!",
            "🐙 Fact: Octopuses have three hearts and blue blood.",
            "🌍 Fact: A day on Venus is longer than a year on Venus.",
            "💻 Fact: The first computer bug was an actual bug — a moth found in a relay in 1947.",
        ],
    ),

    # Current Time 
    Intent(
        name="time",
        patterns=["time", "what time is it", "current time", "what's the time right now"],
        responses=["__TIME__"],   # special token handled by bot
    ),

    # Current Date 
    Intent(
        name="date",
        patterns=["date", "what date is it today", "today's date", "what day is it", "what's the date"],
        responses=["__DATE__"],   # special token handled by bot
    ),

    # Weather (placeholder) 
    Intent(
        name="weather",
        patterns=["weather", "forecast", "temperature", "raining", "sunny"],
        responses=[
            "I don't have live weather data yet, but I'd recommend checking weather.com! ☀️🌧️",
            "My crystal ball is foggy on weather... try a weather app! 🔮",
        ],
    ),

    # Math 
    Intent(
        name="math",
        patterns=["calculate", "math", "compute", "add", "subtract", "multiply", "what is", "divide"],
        responses=["__MATH__"],   # special token handled by bot
    ),

    # Motivational Quotes 
    Intent(
        name="motivation",
        patterns=["motivate me", "inspire me", "quote", "motivation", "encourage"],
        responses=[
            "💪 The only way to do great work is to love what you do. — Steve Jobs",
            "🚀 It does not matter how slowly you go, as long as you do not stop. — Confucius",
            "⭐ Believe you can and you're halfway there. — Theodore Roosevelt",
            "🔥 Act as if what you do makes a difference. It does. — William James",
        ],
    ),

    # Thanks 
    Intent(
        name="thanks",
        patterns=["thank you", "thanks", "thx", "ty", "appreciate", "grateful"],
        responses=[
            "You're very welcome! 😊",
            "Happy to help! Anything else?",
            "Anytime! That's what I'm here for. 🤖",
        ],
    ),

    # Repeat / Memory 
    Intent(
        name="repeat",
        patterns=["repeat", "say again", "what did you say", "last message"],
        responses=["__REPEAT__"],  # special token — bot replays last response
    ),

    # Fallback 
    Intent(
        name="fallback",
        patterns=[],   # catches everything unrecognised
        responses=[
            "Hmm, I'm not sure I understand. Could you rephrase that? 🤔",
            "I don't quite follow. Try asking something else!",
            "That's a tricky one! I'm still learning. 😅",
        ],
    ),
]
