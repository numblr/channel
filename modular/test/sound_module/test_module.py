from unittest import TestCase, main
from modular.modules.modules import Sum, process, Echo, Reverse, Delay,\
    process_sequence
from itertools import islice

STRING_INPUT = "test"
TUPLE_INPUT = ("one", "two", "three")

class ModuleTestCase():
    def test_single(self):
        output = self.module.process(STRING_INPUT).get_output()

        self.assertEquals(output, self.expected_string_input)

    def test_single_list(self):
        output = self.module.process((STRING_INPUT, )).get_output()

        self.assertEquals(output, self.expected_string_input)

    def test_multiple(self):
        output = self.module.process(TUPLE_INPUT).get_output()

        self.assertEquals(output, self.expected_tuple_input)
        
    def test_repeated_process(self):
        for i in range(5):
            self.test_multiple()

    def test_generator(self):
        input_ = (c for c in TUPLE_INPUT)
        output = self.module.process(input_).get_output()

        self.assertEquals(output, self.expected_tuple_input)
        
class NoInputTestCase(object):
    def test_no_input(self):
        self.assertRaises(TypeError, self.module.process, None)

    def test_empty(self):
        output = self.module.process("").get_output()
        self.assertEquals(output, "")

    def test_empty_list(self):
        output = self.module.process(()).get_output()
        self.assertEquals(output, "")

class RepetitionTestCase(object):
    def test_repeated_process(self):
        for i in range(5):
            output = self.module.process(TUPLE_INPUT).get_output()
            self.assertEquals(output, self.expected_tuple_input)

    def test_consecutive_process(self):
        processed = self.module
        for i in range(5):
            processed, value = process(processed, TUPLE_INPUT)
            self.assertEquals(value, self.expected_tuple_input)

class SumTestCase(TestCase, ModuleTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Sum()
        self.expected_string_input = "test"
        self.expected_tuple_input = "onetwothree"

class EchoTestCase(TestCase, ModuleTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Echo()
        self.expected_string_input = "testtest"
        self.expected_tuple_input = "onetwothreeonetwothree"

class ReverseTestCase(TestCase, ModuleTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Reverse()
        self.expected_string_input = "tset"
        self.expected_tuple_input = "eerhtowteno"

class DelayTestCase(TestCase, ModuleTestCase):
    def setUp(self):
        self.module = Delay()
        self.expected_string_input = Delay.INITIAL_VALUE
        self.expected_tuple_input = Delay.INITIAL_VALUE

    def test_no_input(self):
        self.assertRaises(TypeError, self.module.process, None)

    def test_empty(self):
        output = self.module.process("").get_output()
        self.assertEquals(output, Delay.INITIAL_VALUE)

    def test_empty_list(self):
        output = self.module.process(()).get_output()
        self.assertEquals(output, Delay.INITIAL_VALUE)

    def test_repeated_process(self):
        for i in range(5):
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

class HelperFunctionsTestCase(TestCase):
    def test_process(self):
        module = Sum()
        input_ = "test"
        processed_module, output = process(module, input_)
        self.assertEquals(output, module.process(input_).get_output())
        self.assertEquals(processed_module.process(input_).get_output(), module.process(input_).get_output())
    
    def test_process_sequence(self):
        module = Delay()
        input_sequence = ("one", "two", "three")

        output_itr = process_sequence(module, input_sequence)
        
        first_ten_outputs = islice(output_itr, 10)
        expected = (Delay.INITIAL_VALUE, ) + input_sequence + ("", ) * 6
        
        self.assertItemsEqual(first_ten_outputs, expected)
    
    def test_process_sequence_multiple_inputs(self):
        module = Delay()
        input_sequence = (("one", "one"), ("two", "two"), ("three", "three"))

        output_itr = process_sequence(module, input_sequence)
        
        first_ten_outputs = islice(output_itr, 10)
        expected = [Delay.INITIAL_VALUE] + ["oneone", "twotwo", "threethree"] + [""] * 6
        
        self.assertItemsEqual(first_ten_outputs, expected)
    
if __name__ == "__main__":
    main()