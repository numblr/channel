from app.interpreter import Interpreter, EXIT
import logging

_log = logging.getLogger(__name__)

def print_message(error = None):
    print(error if error else "")
    print("Type \"help\" for usage information")

def main():
    print_message()
    interpreter = Interpreter()
    result = 0
    while not result is EXIT:
        try:
            result = interpreter.parse(raw_input(">>> "))
        except ValueError as error:
            print_message(error)
        except RuntimeError as error:
            _log.error("Error happend: ", error)
            return 1
        
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()