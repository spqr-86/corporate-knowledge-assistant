"""Shim package for `adk eval`.

ANCHOR: eval_agent_target
Role: `adk eval` requires an AGENT_MODULE_FILE_PATH directory whose
      __init__.py exposes `agent.root_agent` (see cli_eval.get_root_agent).
      Kept out of the project root so it doesn't turn the whole repo into a
      package and break pytest collection — this is eval-only plumbing.
"""

from . import agent as agent
