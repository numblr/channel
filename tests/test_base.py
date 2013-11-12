from modular.channels.channels import sum_channel, init_channel
from modular.test.channels.base import ChannelTestCase, RepetitionTestCase, \
    NoInputTestCase
from unittest import TestCase, main

class SumTestCase(TestCase, ChannelTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.channel = init_channel(sum_channel)
        self.expected_string_input = "test"
        self.expected_tuple_input = "onetwothree"
        self.expected_no_input = ""

if __name__ == "__main__":
    main()