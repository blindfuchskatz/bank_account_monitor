import sys

class Logger:
    def error(self, msg: str) -> None:
        print(msg, file=sys.stderr)
