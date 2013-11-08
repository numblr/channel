from app.Interpreter import Interpreter, EXIT
import logging

_log = logging.getLogger(__name__)

_USAGE = """
module <name> <operation>
connection <name_1> <name_2>
process <string>...
"""

def print_usage(error = None):
    print(error if error else "")
    print(_USAGE)

def main():
    print_usage()
    interpreter = Interpreter()
    result = 0
    while not result is EXIT:
        try:
            result = interpreter.parse(raw_input(">>> "))
        except ValueError as error:
            print_usage(error)
        except RuntimeError as error:
            _log.error("Error happend: ", error)
            return 1
        
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()