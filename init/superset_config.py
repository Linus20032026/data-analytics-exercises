"""
Custom Superset configuration — loaded via SUPERSET_CONFIG_PATH.
Patches FAB SecurityManager so create_all() uses checkfirst=True,
making the startup sequence idempotent across container restarts.
"""

import sqlalchemy as sa
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_appbuilder.security.sqla.manager import SecurityManager
from superset.security import SupersetSecurityManager


class IdempotentSecurityManager(SupersetSecurityManager):
    """Same as SupersetSecurityManager but _create_db is safe to call repeatedly."""

    def _create_db(self) -> None:
        engine = self.session.get_bind(mapper=None, clause=None)
        inspector = sa.inspect(engine)
        existing = inspector.get_table_names()
        if "ab_user" not in existing or "ab_group" not in existing:
            from flask_appbuilder.models.sqla import Model
            Model.metadata.create_all(engine, checkfirst=True)
        # Call BaseSecurityManager.create_db (sets up roles/permissions, no recursive _create_db)
        BaseSecurityManager.create_db(self)


CUSTOM_SECURITY_MANAGER = IdempotentSecurityManager
