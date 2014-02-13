from ..numeric_channels import sum_channel, inverse_channel, moving_average_channel
from unittest import TestCase, main
from .base import ChannelTestCase, NoInputTestCase,\
    MemorylessTestCase

class SumTestCase(TestCase, ChannelTestCase, NoInputTestCase, MemorylessTestCase):
    def setUp(self):
        self.channel = sum_channel()
        self.single_input = 1
        self.tuple_input = (1, 2, 3)
        self.expected_single_input = 1
        self.expected_tuple_input = 6
        self.expected_no_input = 0
        self.empty_val = 0

class InverseTestCase(TestCase, ChannelTestCase, NoInputTestCase, MemorylessTestCase):
    def setUp(self):
        self.channel = inverse_channel(4)
        self.single_input = 1
        self.tuple_input = (1, 2, 3)
        self.expected_single_input = -1
        self.expected_tuple_input = -6
        self.expected_no_input = 0
        self.empty_val = 0

class MovingAverageTestCase(TestCase, ChannelTestCase, NoInputTestCase):
    def setUp(self):
        self.channel = moving_average_channel(4)
        self.single_input = 8
        self.tuple_input = (1, 2, 3, 4, 5, 5) # sum = 20
        self.expected_single_input = 2
        self.expected_tuple_input = 5
        self.expected_no_input = 0
        self.empty_val = 0
    
    def testAverage(self):
        averages_input = (self.channel.send(i) for i in range(4, 25, 4))
        averages_zeros = (self.channel.send(i) for i in (0, ) * 5)
        all_averages = tuple(averages_input) + tuple(averages_zeros)

        expected = (1.0, 3.0, 6.0, 10.0, 14.0, 18.0, 15.0, 11.0, 6.0, 0.0, 0.0)

        self.assertSequenceEqual(expected, all_averages)


#class HelperFunctionsTestCase(TestCase):
#    def test_None_values(self):
#        channel = memoryless_channel()
#        input_sequence = chain(("one", None, "three"), iter(lambda: None, ()))
#        
#        output_itr = process_sequence(channel, input_sequence)
#        
#        first_ten_outputs = islice(output_itr, 10)
#        expected = ("one", "", "three" ) + ("", ) * 7
#        
#        self.assertCountEqual(first_ten_outputs, expected)
#    
#    def test_process_sequence(self):
#        channel = delay_channel()
#        input_sequence = ("one", "two", "three")
#
#        output_itr = process_sequence(channel, input_sequence)
#        
#        first_ten_outputs = islice(output_itr, 10)
#        expected = (DELAY_INITIAL, ) + input_sequence + ("", ) * 6
#        
#        self.assertCountEqual(first_ten_outputs, expected)
#    
#    def test_process_sequence_multiple_inputs(self):
#        channel = delay_channel()
#        input_sequence = (("one", "one"), ("two", "two"), ("three", "three"))
#
#        output_itr = process_sequence(channel, input_sequence)
#        
#        first_ten_outputs = islice(output_itr, 10)
#
#        expected = [DELAY_INITIAL] + ["oneone", "twotwo", "threethree"] + [""] * 6
#        
#        self.assertCountEqual(first_ten_outputs, expected)

if __name__ == "__main__":
    main()    