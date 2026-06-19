"""
test_chatbot.py

Unit test suite for the modular, rule-based chatbot.
Tests intent matching, conversation memory, math logic, and chatbot responses.
"""

import unittest
from datetime import datetime
from chatbot.intents import Intent, INTENTS
from chatbot.matcher import IntentMatcher
from chatbot.memory import ConversationMemory, MemoryEntry
from chatbot.bot import Chatbot


class TestIntentMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = IntentMatcher()

    def test_greeting_match(self):
        intent, confidence = self.matcher.match("hello there")
        self.assertEqual(intent.name, "greeting")
        self.assertGreater(confidence, 0.5)

    def test_farewell_match(self):
        intent, confidence = self.matcher.match("quit now please")
        self.assertEqual(intent.name, "farewell")
        self.assertGreater(confidence, 0.5)

    def test_math_match(self):
        intent, confidence = self.matcher.match("calculate 5 plus 10")
        self.assertEqual(intent.name, "math")
        self.assertGreater(confidence, 0.5)

    def test_fallback_match(self):
        # random gibberish should trigger fallback
        intent, confidence = self.matcher.match("xyzqwertyyuiop")
        self.assertEqual(intent.name, "fallback")
        self.assertEqual(confidence, 0.0)


class TestConversationMemory(unittest.TestCase):
    def setUp(self):
        self.memory = ConversationMemory(max_turns=5)

    def test_memory_sliding_window(self):
        for i in range(6):
            self.memory.add_user(f"message {i}")
        recent = self.memory.recent_turns()
        self.assertEqual(len(recent), 5)
        self.assertEqual(recent[-1].text, "message 5")

    def test_context_management(self):
        self.memory.context = "test_context"
        self.assertEqual(self.memory.context, "test_context")


class TestChatbot(unittest.TestCase):
    def setUp(self):
        self.bot = Chatbot(name="TestNexus")

    def test_name_response(self):
        reply = self.bot.respond("what is your name")
        self.assertTrue(any(name in reply for name in ["Nexus", "TestNexus"]))

    def test_math_calculation(self):
        reply = self.bot.respond("calculate 15 + 35")
        self.assertIn("50", reply)

        reply2 = self.bot.respond("calculate 100 divided by 4")
        self.assertIn("25", reply2)

        # Division by zero
        reply3 = self.bot.respond("calculate 10 / 0")
        self.assertIn("zero", reply3.lower())

    def test_repeat_logic(self):
        first_reply = self.bot.respond("tell me a fun fact")
        repeat_reply = self.bot.respond("repeat what you just said")
        self.assertIn(first_reply, repeat_reply)


if __name__ == "__main__":
    unittest.main()
