import os
import sys
import socket

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "creatorhub.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)
    
    execute_from_command_line([sys.argv[0], "runserver", f"{IP}:8080"])

if __name__ == "__main__":
    main()
