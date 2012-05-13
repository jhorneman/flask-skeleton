import sys
from application import create_app, run_app

if __name__ == "__main__":
    if len(sys.argv) > 1:
        create_app(sys.argv[1])
    else:
        create_app()
    run_app()
