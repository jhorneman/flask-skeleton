import sys
from application import run_app

if __name__ == "__main__":
	if len(sys.argv) > 1:
		run_app(sys.argv[1])
	else:
		run_app()
