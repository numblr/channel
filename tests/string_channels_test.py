from itertools import islice, chain
from modular.channels.string_channels import echo_channel, reverse_channel, \
    delay_channel, DELAY_INITIAL, process_sequence, sum_channel
from unittest import TestCase, main
from modular.test.channels.base import ChannelTestCase, NoInputTestCase,\
    MemorylessTestCase
from modular.channels.channels import memoryless_channel

class SumTestCase(TestCase, ChannelTestCase, NoInputTestCase, MemorylessTestCase):
    def setUp(self):
        self.channel = sum_channel()
        self.expected_string_input = "test"
        self.expected_tuple_input = "onetwothree"
        self.expected_no_input = ""

class EchoTestCase(TestCase, ChannelTestCase, NoInputTestCase, MemorylessTestCase):
    def setUp(self):
        self.channel = echo_channel()
        self.expected_string_input = "testtest"
        self.expected_tuple_input = "onetwothreeonetwothree"
        self.expected_no_input = ""

class ReverseTestCase(TestCase, ChannelTestCase, NoInputTestCase, MemorylessTestCase):
    def setUp(self):
        self.channel = reverse_channel()
        self.expected_string_input = "tset"
        self.expected_tuple_input = "eerhtowteno"
        self.expected_no_input = ""

class DelayTestCase(TestCase, ChannelTestCase):
    def setUp(self):
        self.channel = delay_channel()
        self.expected_string_input = DELAY_INITIAL
        self.expected_tuple_input = DELAY_INITIAL
        self.expected_no_input = DELAY_INITIAL

    def test_consecutive_process(self):
        input_ = ("t", "e", "s", "t", "", "", "", "")
        expected = (DELAY_INITIAL, "t", "e", "s", "t", "", "", "")
        
        self.__test_consecutive_process(input_, expected)

    def __test_consecutive_process_multiple(self):
        input_ = (("o", "n", "e"), ("t", "w", "o"), ("t", "h", "r", "e", "e"), (), (), (), ())
        expected = (DELAY_INITIAL, "one", "two", "three", "", "", "")
        
        self.__test_consecutive_process(input_, expected)
        
    def __test_consecutive_process(self, input_, expected):
        for input_value, expected_output in zip(input_, expected):
            output = self.channel.send(input_value)
            self.assertEquals(output, expected_output)

class HelperFunctionsTestCase(TestCase):
    def test_None_values(self):
        channel = memoryless_channel()
        input_sequence = chain(("one", None, "three"), iter(lambda: None, ()))
    
        output_itr = process_sequence(channel, input_sequence)

        first_ten_outputs = islice(output_itr, 10)
        expected = ("one", "", "three" ) + ("", ) * 7
        
        self.assertItemsEqual(first_ten_outputs, expected)
        
    def test_process_sequence(self):
        channel = delay_channel()
        input_sequence = ("one", "two", "three")

        output_itr = process_sequence(channel, input_sequence)
        
        first_ten_outputs = islice(output_itr, 10)
        expected = (DELAY_INITIAL, ) + input_sequence + ("", ) * 6
        
        self.assertItemsEqual(first_ten_outputs, expected)
    
    def test_process_sequence_multiple_inputs(self):
        channel = delay_channel()
        input_sequence = (("one", "one"), ("two", "two"), ("three", "three"))

        output_itr = process_sequence(channel, input_sequence)
        
        first_ten_outputs = islice(output_itr, 10)

        expected = [DELAY_INITIAL] + ["oneone", "twotwo", "threethree"] + [""] * 6
        
        self.assertItemsEqual(first_ten_outputs, expected)

if __name__ == "__main__":
    main()    