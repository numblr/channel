import unittest
from app.app_config import COMMANDS, ArgumentError
from app.interpreter import EXIT

NO_ARG = " "
ONE_ARG = "test"
TWO_ARG = "test test"
THREE_ARG = "test test"

ONE_EXPECTED = "1 arguments expected"
TWO_EXPECTED = "2 arguments expected"

class Test(unittest.TestCase):
    def test_argument_numbers(self):
        for command in (COMMANDS["module"], COMMANDS["connect"]):
            self.assertRaisesRegexp(ArgumentError, TWO_EXPECTED ,command, ONE_ARG)
            self.assertRaisesRegexp(ArgumentError, TWO_EXPECTED, command, THREE_ARG)
            
        for command in (COMMANDS["define"], ):
            self.assertRaisesRegexp(ArgumentError,ONE_EXPECTED ,command, NO_ARG)
            self.assertRaisesRegexp(ArgumentError, ONE_EXPECTED, command, TWO_ARG)

    def test_exit(self):
        self.assertIs(COMMANDS["exit"], EXIT)

if __name__ == "__main__":
    unittest.main()