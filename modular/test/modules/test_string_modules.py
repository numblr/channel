from modular.test.modules.base import ModuleTestCase, NoInputTestCase,\
    RepetitionTestCase, TUPLE_INPUT
from unittest.case import TestCase
from modular.modules.string_modules import Echo, Reverse, Delay
from modular.modules.base import process

class EchoTestCase(TestCase, ModuleTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Echo()
        self.expected_string_input = "testtest"
        self.expected_tuple_input = "onetwothreeonetwothree"
        self.expected_no_input = ""

class ReverseTestCase(TestCase, ModuleTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Reverse()
        self.expected_string_input = "tset"
        self.expected_tuple_input = "eerhtowteno"
        self.expected_no_input = ""

class DelayTestCase(TestCase, ModuleTestCase):
    def setUp(self):
        self.module = Delay()
        self.expected_string_input = Delay.INITIAL_VALUE
        self.expected_tuple_input = Delay.INITIAL_VALUE
        self.expected_no_input = Delay.INITIAL_VALUE

    def test_repeated_process(self):
        for _ in range(5):
            output = self.module.process(TUPLE_INPUT).get_output()
            self.assertEquals(output, Delay.INITIAL_VALUE)

    def test_consecutive_process(self):
        input_ = ("t", "e", "s", "t", "", "", "", "")
        expected = (Delay.INITIAL_VALUE, "t", "e", "s", "t", "", "", "")
        
        self.__test_consecutive_process(input_, expected)

    def __test_consecutive_process_multiple(self):
        input_ = (("o", "n", "e"), ("t", "w", "o"), ("t", "h", "r", "e", "e"), (), (), (), ())
        expected = (Delay.INITIAL_VALUE, "one", "two", "three", "", "", "")
        
        self.__test_consecutive_process(input_, expected)
        
    def __test_consecutive_process(self, input_, expected):
        processed = self.module
        
        for input_value, expected_output in zip(input_, expected):
            processed, output = process(processed, input_value)
            self.assertEquals(output, expected_output)

