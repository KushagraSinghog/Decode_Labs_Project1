"""
main.py

Entry point — runs the chatbot in an interactive terminal loop.

Features:

    • Styled banner with bot name and commands
    • Continuous input loop with graceful exit
    • Displays confidence score and context after each reply
    • Prints session summary on exit
    • Handles KeyboardInterrupt (Ctrl-C) cleanly
"""

from __future__ import annotations

# Windows: ensure stdout is UTF-8 so emojis & special chars render correctly
import io
import sys
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

from chatbot import Chatbot
from chatbot.logger import get_logger

log = get_logger("main")


# ANSI styling helpers

def _c(text: str, code: str) -> str:
    """Wrap text in an ANSI colour code (auto-reset)."""
    return f"\033[{code}m{text}\033[0m"

CYAN    = lambda t: _c(t, "96")
GREEN   = lambda t: _c(t, "92")
YELLOW  = lambda t: _c(t, "93")
MAGENTA = lambda t: _c(t, "95")
BOLD    = lambda t: _c(t, "1")
DIM     = lambda t: _c(t, "2")


# Banner

BANNER = f"""
{CYAN('╔══════════════════════════════════════════════════════╗')}
{CYAN('║')}   {BOLD('🤖  N E X U S  —  Rule-Based AI Chatbot')}            {CYAN('║')}
{CYAN('║')}   {DIM('Modular • Intent Matching • Memory • Logging')}        {CYAN('║')}
{CYAN('╠══════════════════════════════════════════════════════╣')}
{CYAN('║')}  Commands: {GREEN('help')}  {GREEN('history')}  {GREEN('summary')}  {YELLOW('exit / bye')}          {CYAN('║')}
{CYAN('╚══════════════════════════════════════════════════════╝')}
"""


# Main loop

def main() -> None:
    print(BANNER)
    bot = Chatbot(name="Nexus")
    log.info("Session started.")

    while True:
        # Read user input 
        try:
            user_input = input(f"{GREEN('You')} » ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{YELLOW('Session interrupted. Goodbye!')} 👋")
            log.info("Session interrupted by user (Ctrl-C / EOF).")
            break

        if not user_input:
            continue

        # Local meta-commands 
        if user_input.lower() == "history":
            entries = bot.history(n=10)
            print(f"\n{CYAN('── Last 10 turns ──')}")
            for e in entries:
                print(f"  {DIM(str(e))}")
            print()
            continue

        if user_input.lower() == "summary":
            print(f"\n{CYAN('── Session Summary ──')}")
            print(f"  {bot.session_summary()}\n")
            continue

        # Get bot reply 
        reply = bot.respond(user_input)
        print(f"\n{MAGENTA(bot.name)} » {reply}\n")

        # Exit gate 
        if bot.is_exit_requested:
            log.info("Exit intent detected. Ending session.")
            print(f"{DIM(bot.session_summary())}\n")
            break

    log.info("Session ended.")
    print(DIM("Thanks for chatting! Logs saved to logs/chatbot.log"))


# Entry guard

if __name__ == "__main__":
    main()
