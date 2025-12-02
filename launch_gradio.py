"""Launcher script for Gradio UI."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run
from src.app_gradio import main

if __name__ == "__main__":
    main()
