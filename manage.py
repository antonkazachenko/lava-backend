#!/usr/bin/env python
import os
import sys
sys.setrecursionlimit(1500)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lava_api.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and available on your PYTHONPATH, "
            "and that you have activated a virtual environment."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
