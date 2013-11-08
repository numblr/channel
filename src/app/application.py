from app.Interpreter import Interpreter
def main():
    interpreter = Interpreter()
    while True:
        interpreter.parse(raw_input(">>> "))
        
    return 0

if __name__ == "__main__":
    main()