from ..array_channels import sum_channel, moving_average_channel
from unittest import TestCase, main
import numpy as np
from numpy.testing import assert_array_equal

class ChannelTestCase():
    def test_single(self):
        output = self.channel.send(self.single_input)

        assert_array_equal(output, self.expected_single_input)

    def test_single_list(self):
        output = self.channel.send((self.single_input, ))

        assert_array_equal(output, self.expected_single_input)

    def test_multiple(self):
        output = self.channel.send(self.tuple_input)

        assert_array_equal(output, self.expected_tuple_input)
        
    def test_generator(self):
        input_ = (c for c in self.tuple_input)
        output = self.channel.send(input_)

        assert_array_equal(output, self.expected_tuple_input)
        
class NoInputTestCase():
    def test_no_input(self):
        self.assertRaises(TypeError, self.channel.send, None)

    def test_empty(self):
        output = self.channel.send(self.empty_val)
        assert_array_equal(output, self.expected_no_input)

    def test_empty_list(self):
        output = self.channel.send(())
        assert_array_equal(output, self.expected_no_input)

class MemorylessTestCase():
    def test_repeated_send(self):
        for i in range(5):
            output = self.channel.send(self.tuple_input)
            assert_array_equal(output, self.expected_tuple_input, "Failed at {0}".format(i))

    def test_consecutive_send(self):
        for i in range(5):
            value = self.channel.send(self.tuple_input)
            assert_array_equal(value, self.expected_tuple_input, "Failed at {0}".format(i))



class SumTestCase(TestCase, ChannelTestCase, NoInputTestCase, MemorylessTestCase):
    def setUp(self):
        self.channel = sum_channel()
        self.single_input = (1, 2, 3)
        self.tuple_input = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
        self.expected_single_input = (1, 2, 3)
        self.expected_tuple_input = (12, 15, 18)
        self.expected_no_input = ()
        self.empty_val = ()

class MovingAverageTestCase(TestCase, ChannelTestCase, NoInputTestCase):
    def setUp(self):
        self.channel = moving_average_channel(4)
        self.single_input = (4, 8, 16)
        self.tuple_input = ((1, 2, 3), (4, 6, 8), (7, 8, 9))
        self.expected_single_input = (1, 2, 4)
        self.expected_tuple_input = (3, 4, 5)
        self.expected_no_input = 0
        self.empty_val = ()
    
    def testAverage(self):
        input_arrays = np.ones((3, 6)) * np.array([i for i in range(4, 25, 4)])
        averages_input = [self.channel.send(i) for i in input_arrays.T]
        averages_zeros = [self.channel.send(i) for i in np.zeros((5, 3))]
        
        expected_avg_input = (np.ones((3)) * 1.0, \
                              np.ones((3)) * 3.0, \
                              np.ones((3)) * 6.0, \
                              np.ones((3)) * 10.0, \
                              np.ones((3)) * 14.0, \
                              np.ones((3)) * 18.0)

        expected_avg_zeros = (np.ones((3)) * 15.0, \
                              np.ones((3)) * 11.0, \
                              np.ones((3)) * 6.0, \
                              np.ones((3)) * 0.0, \
                              np.ones((3)) * 0.0)
        
        assert_array_equal(expected_avg_input, averages_input)
        assert_array_equal(expected_avg_zeros, averages_zeros)
        
if __name__ == '__main__':
    main()