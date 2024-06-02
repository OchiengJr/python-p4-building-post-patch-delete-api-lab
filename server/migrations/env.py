from __future__ import with_statement

import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# Load the Alembic configuration file
config = context.config

# Interpret the configuration file for Python logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Set the SQLAlchemy URL for migrations
config.set_main_option(
    'sqlalchemy.url',
    str(current_app.extensions['migrate'].db.get_engine().url).replace('%', '%%')
)

# Define the target metadata
target_metadata = current_app.extensions['migrate'].db.metadata

# Define the offline migration function
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# Define the online migration function
def run_migrations_online():
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = current_app.extensions['migrate'].db.get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine whether to run migrations offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
