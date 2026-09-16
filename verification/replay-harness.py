#!/usr/bin/env python3
"""Canonical replay entry point.

This wrapper intentionally imports the canonical underscore-named
orchestrator.
"""

from run_all import main


if __name__ == "__main__":
    raise SystemExit(main())
