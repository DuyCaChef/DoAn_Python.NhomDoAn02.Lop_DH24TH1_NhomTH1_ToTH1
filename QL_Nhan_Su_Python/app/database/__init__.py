"""Proxy package so code can import `app.database` while real modules live in `database/`.

This module exposes `db_init`, `db_config`, and `queries` by importing the project-level
`database` package. It handles different import contexts (running as script or package).
"""
"""app.database package: expose local DB modules."""
from . import db_init, db_config, connection, queries

__all__ = ["db_init", "db_config", "connection", "queries"]
