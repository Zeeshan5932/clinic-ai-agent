"""
Compatibility shim package.

Allows importing `app.*` when the current working directory is `backend/app`
and uvicorn is started with `app.main:app`.
"""
from pathlib import Path

_package_dir = Path(__file__).resolve().parent
_project_app_dir = _package_dir.parent

# Prefer the real project app directory for submodule resolution (main, core, api, ...).
__path__ = [str(_project_app_dir), str(_package_dir)]
