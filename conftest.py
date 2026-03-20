import sys
from pathlib import Path

# Add src/ to sys.path so tests can import ee_agent without installation
sys.path.insert(0, str(Path(__file__).parent / "src"))
