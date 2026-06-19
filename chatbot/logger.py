"""
logger.py

ChatLogger — centralised logging for the chatbot.

Two output targets:
  1. Console handler  → INFO level, colourised via ANSI codes
  2. File handler     → DEBUG level, plain text, saved to logs/chatbot.log

Usage:

    from chatbot.logger import get_logger
    log = get_logger(__name__)
    log.info("Hello")
    log.debug("Debug detail")
"""

from __future__ import annotations

import codecs
import io
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


# ANSI colour helpers (console only)

class _ColourFormatter(logging.Formatter):
    """Adds ANSI colour codes to log level names for terminal output."""

    COLOURS = {
        logging.DEBUG:    "\033[36m",    # cyan
        logging.INFO:     "\033[32m",    # green
        logging.WARNING:  "\033[33m",    # yellow
        logging.ERROR:    "\033[31m",    # red
        logging.CRITICAL: "\033[35m",    # magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        colour = self.COLOURS.get(record.levelno, self.RESET)
        record.levelname = f"{colour}{record.levelname:<8}{self.RESET}"
        return super().format(record)


# Logger factory

_LOG_DIR  = Path("logs")
_LOG_FILE = _LOG_DIR / "chatbot.log"
_INIT_DONE = False   # ensure handlers are added only once


def _bootstrap() -> None:
    """Create log directory and attach handlers to the root 'chatbot' logger."""
    global _INIT_DONE
    if _INIT_DONE:
        return
    _INIT_DONE = True

    _LOG_DIR.mkdir(exist_ok=True)

    root = logging.getLogger("chatbot")
    root.setLevel(logging.DEBUG)          # capture everything; handlers filter

    # Console handler (UTF-8 safe on Windows) 
    _utf8_stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
    )
    ch = logging.StreamHandler(_utf8_stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(_ColourFormatter(
        fmt="%(asctime)s  %(levelname)s  %(name)s :: %(message)s",
        datefmt="%H:%M:%S",
    ))
    root.addHandler(ch)

    # File handler (rotating, max 1 MB, keep 3 backups) 
    fh = RotatingFileHandler(
        _LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s :: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root.addHandler(fh)

    root.info("Logger initialised - writing to %s", _LOG_FILE.resolve())


def get_logger(name: str) -> logging.Logger:
    """
    Return a child logger under the 'chatbot' namespace.

    Parameters
    ----------
    name : typically __name__ of the calling module
    """
    _bootstrap()
    return logging.getLogger(f"chatbot.{name}")
