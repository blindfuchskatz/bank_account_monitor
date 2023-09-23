import sys

class Logger:
    def error(self, msg):
        print(msg, file=sys.stderr)
