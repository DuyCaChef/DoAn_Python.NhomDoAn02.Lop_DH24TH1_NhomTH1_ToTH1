"""app package for refactored HRM project.
This package provides a clear structure mirroring the requested template.
"""

# Re-export commonly used modules for convenience
from . import controllers, database, models, views

__all__ = ["controllers", "database", "models", "views"]
