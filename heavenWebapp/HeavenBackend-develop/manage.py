#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from heaven.settings import base

scheduler = BackgroundScheduler()
# db_url = "mysql://root:digital23!@localhost:3307/heaven"
# jobstore = {"default": SQLAlchemyJobStore(url=db_url)}
# scheduler.add_jobstore(jobstore["default"], alias="default")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "heaven.settings.base")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    scheduler.start()
    main()
