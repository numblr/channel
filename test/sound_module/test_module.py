from unittest import TestCase, main
from sound_module.modules import Sum, process, Echo, Reverse, Delay

STRING_INPUT = "test"
TUPLE_INPUT = ("one", "two", "three")

class ModuleTestCase():
    def test_single(self):
        processed, value = process(self.module, STRING_INPUT)

        self.assertEquals(value, self.expected_string_input)

    def test_single_list(self):
        processed, value = process(self.module, (STRING_INPUT, ))

        self.assertEquals(value, self.expected_string_input)

    def test_multiple(self):
        processed, value = process(self.module, TUPLE_INPUT)

        self.assertEquals(value, self.expected_tuple_input)
        
    def test_repeated_process(self):
        for i in range(5):
            self.test_multiple()

    def test_generator(self):
        input_ = (c for c in TUPLE_INPUT)
        processed, value = process(self.module, input_)

        self.assertEquals(value, self.expected_tuple_input)
        
class NoInputTestCase(object):
    def test_no_input(self):
        self.assertRaises(TypeError, self.module.process, None)

    def test_empty(self):
        processed, value = process(self.module, "")
        self.assertEquals(value, "")

    def test_empty_list(self):
        processed, value = process(self.module, ())
        self.assertEquals(value, "")

class RepetitionTestCase(object):
    def test_repeated_process(self):
        for i in range(5):
            processed, value = process(self.module, TUPLE_INPUT)
            self.assertEquals(value, self.expected_tuple_input)

    def test_consecutive_process(self):
        processed = self.module
        for i in range(5):
            processed, value = process(processed, TUPLE_INPUT)
            self.assertEquals(value, self.expected_tuple_input)

class TestSum(TestCase, ModuleTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Sum()
        self.expected_string_input = "test"
        self.expected_tuple_input = "onetwothree"

class TestEcho(TestCase, ModuleTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Echo()
        self.expected_string_input = "testtest"
        self.expected_tuple_input = "onetwothreeonetwothree"

class TestReverse(TestCase, ModuleTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Reverse()
        self.expected_string_input = "tset"
        self.expected_tuple_input = "eerhtowteno"

class TestDelay(TestCase, ModuleTestCase):
    def setUp(self):
        self.module = Delay()
        self.expected_string_input = Delay.INITIAL_VALUE
        self.expected_tuple_input = Delay.INITIAL_VALUE

    def test_no_input(self):
        self.assertRaises(TypeError, self.module.process, None)

    def test_empty(self):
        processed, value = process(self.module, "")
        self.assertEquals(value, Delay.INITIAL_VALUE)

    def test_empty_list(self):
        processed, value = process(self.module, ())
        self.assertEquals(value, Delay.INITIAL_VALUE)

    def test_repeated_process(self):
        for i in range(5):
            processed, value = process(self.module, TUPLE_INPUT)
            self.assertEquals(value, Delay.INITIAL_VALUE)

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
        
        for input_value, expected_value in zip(input_, expected):
            processed, value = process(processed, input_value)
            self.assertEquals(value, expected_value)
            
if __name__ == "__main__":
    main()