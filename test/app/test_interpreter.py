import unittest
from app.interpreter import Interpreter, CommandError, EXIT

TEST_COMMANDS = {"one": lambda state, *args: state.append("one called with " + " ".join(args)),
                 "two": lambda state, *args: state.append("two called with " + " ".join(args)),
                 "quit": EXIT
                 }

class InterpreterTestCase(unittest.TestCase):
    def setUp(self):
        self.state = []
        self.interpreter = Interpreter(self.state, TEST_COMMANDS)
    
    def test_no_input(self):
        initial = list(self.state)
        self.interpreter.parse("")
        self.interpreter.parse(" \t")
        
        self.assertEquals(self.state, initial)

    def test_command(self):
        self.interpreter.parse("one argone argtwo")
        
        self.assertEquals(self.state, ["one called with argone argtwo"])

    def test_several_commands(self):
        self.interpreter.parse("one argone argtwo")
        self.interpreter.parse("two argone")
        
        self.assertEquals(self.state, ["one called with argone argtwo", "two called with argone"])

    def test_several_exit(self):
        self.assertIs(self.interpreter.parse("quit 1 2 3"), EXIT)

    def test_undefined_command(self):
        self.assertRaisesRegexp(CommandError, "test", self.interpreter.parse, "test argone argtwo")

if __name__ == "__main__":
    unittest.main()