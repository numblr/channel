from itertools import islice
from modular.modules.base import Sum, process, process_sequence
from modular.modules.string_modules import Delay
from modular.test.modules.base import ModuleTestCase, RepetitionTestCase, \
    NoInputTestCase
from unittest import TestCase, main

class SumTestCase(TestCase, ModuleTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Sum()
        self.expected_string_input = "test"
        self.expected_tuple_input = "onetwothree"
        self.expected_no_input = ""

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