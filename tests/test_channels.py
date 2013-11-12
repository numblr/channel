from itertools import islice
from modular.channels.channels import init_channel
from modular.channels.string_channels import echo_channel, reverse_channel, \
    delay_channel, DELAY_INITIAL, sum_channel, multi_input_channel
from modular.test.channels.base import ChannelTestCase, NoInputTestCase, \
    RepetitionTestCase, TUPLE_INPUT
from unittest import TestCase, main

class EchoTestCase(TestCase, ChannelTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.channel = init_channel(multi_input_channel(echo_channel))
        self.expected_string_input = "testtest"
        self.expected_tuple_input = "onetwothreeonetwothree"
        self.expected_no_input = ""

class ReverseTestCase(TestCase, ChannelTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.channel = init_channel(multi_input_channel(reverse_channel))
        self.expected_string_input = "tset"
        self.expected_tuple_input = "eerhtowteno"
        self.expected_no_input = ""

class DelayTestCase(TestCase, ChannelTestCase):
    def setUp(self):
        self.channel = init_channel(delay_channel)
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

#class HelperFunctionsTestCase(TestCase):
#    def test_process(self):
#        channel = init_channel(sum_channel)
#        input_ = "test"
#        processed_channel, output = channel.send(input_)
#        self.assertEquals(output, channel.send(input_))
#        self.assertEquals(processed_channel.send(input_), channel.send(input_))
#    
#    def test_process_sequence(self):
#        channel = init_channel(delay_channel)
#        input_sequence = ("one", "two", "three")
#
#        output_itr = process_sequence(channel, input_sequence)
#        
#        first_ten_outputs = islice(output_itr, 10)
#        expected = (DELAY_INITIAL, ) + input_sequence + ("", ) * 6
#        
#        self.assertItemsEqual(first_ten_outputs, expected)
#    
#    def test_process_sequence_multiple_inputs(self):
#        channel = init_channel(delay_channel)
#        input_sequence = (("one", "one"), ("two", "two"), ("three", "three"))
#
#        output_itr = process_sequence(channel, input_sequence)
#        
#        first_ten_outputs = islice(output_itr, 10)
#        expected = [DELAY_INITIAL] + ["oneone", "twotwo", "threethree"] + [""] * 6
#        
#        self.assertItemsEqual(first_ten_outputs, expected)

if __name__ == "__main__":
    main()    