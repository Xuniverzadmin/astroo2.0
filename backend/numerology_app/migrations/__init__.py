"""
Migrations package for the numerology application.

This package contains database migration scripts and utilities.
For now, we use simple Base.metadata.create_all() in startup events,
but this can be extended to use Alembic for more complex migrations.
"""

# This file makes the migrations directory a Python package
