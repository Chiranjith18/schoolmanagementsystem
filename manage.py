#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def create_superuser():
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print("✅ Superuser created")
    except Exception as e:
        print("⚠️ Superuser creation skipped:", e)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schoolmanagement.settings")
    try:
        from django.core.management import execute_from_command_line
        import django
        django.setup()

        # 👇 CREATE SUPERUSER AFTER DJANGO SETUP
        create_superuser()

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
