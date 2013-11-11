from modular.modules.base import Sum
from modular.test.modules.base import ModuleTestCase, RepetitionTestCase, \
    NoInputTestCase
from unittest import TestCase, main

class SumTestCase(TestCase, ModuleTestCase, NoInputTestCase, RepetitionTestCase):
    def setUp(self):
        self.module = Sum()
        self.expected_string_input = "test"
        self.expected_tuple_input = "onetwothree"
        self.expected_no_input = ""

if __name__ == "__main__":
    main()