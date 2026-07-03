"""Re-exports the real root_agent for `adk eval` — see __init__.py.

`adk eval` loads this package's __init__.py under sys.modules["agent"],
which would shadow the project's real agent.py on a plain `from agent
import root_agent` (name collision, not a real reimport). Load the real
file by explicit path instead.
"""

import importlib.util
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_spec = importlib.util.spec_from_file_location(
    "_corporate_knowledge_assistant_agent_impl", _PROJECT_ROOT / "agent.py"
)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

root_agent = _module.root_agent
