#!/usr/bin/env python3
"""
Entry point for CLI execution.

Usage:
  python -m core.cli generate --topic "Your Topic"
  
Or directly:
  ./cli.py generate --topic "Your Topic"
"""

from core.cli import main

if __name__ == "__main__":
    main()
