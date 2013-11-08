from app.Interpreter import Interpreter
import logging
def main():
    interpreter = Interpreter()
    while True:
        interpreter.parse(raw_input(">>> "))
        
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()