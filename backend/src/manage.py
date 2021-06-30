#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os.path
import sys


def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    command_name = sys.argv[-1].lower().strip()
    if command_name == "startapp":
        app_name = input("Enter app name: ")
        apps_base_dir = "./api/apps"
        if not os.path.exists(apps_base_dir):
            os.mkdir(apps_base_dir)
            open(f"{apps_base_dir}/__init__.py", "w").close()

        app_dir = f"{apps_base_dir}/{app_name}"
        if not os.path.isdir(app_dir):
            os.mkdir(app_dir)

        execute_from_command_line(sys.argv + [app_name, app_dir])
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
