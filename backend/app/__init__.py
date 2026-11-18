import sys
from pathlib import Path

# Support both `uvicorn backend.app.main:app` from the project root and
# `uvicorn app.main:app` from inside the backend directory.
_BACKEND_ROOT = str(Path(__file__).resolve().parents[1])
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)
