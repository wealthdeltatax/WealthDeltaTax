"""Put pipeline/ on sys.path (its modules import each other by bare name)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
FIXTURES = Path(__file__).resolve().parent / "fixtures"
