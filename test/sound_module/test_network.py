from unittest import TestCase, main
from sound_module.network import Network
#from sound_module.test_module import ModuleTestCase
from sound_module.modules import process, Delay, Reverse, Sum
from collections import OrderedDict

MODULES = (("a", Sum()), ("b", Reverse()), ("c", Delay()))
CONNECTIONS = {"b": "a", "c": "b"} 

class TestNetwork(TestCase):
    def setUp(self):
        self.module = Network(MODULES, CONNECTIONS)
        
    def test_consecutive_process(self):
        input_ = ("hello", "world", "", "", "", "")
        expected = (Delay.INITIAL_VALUE, "olleh", "dlrow", "", "")
        
        self.__test_consecutive_process(input_, expected)
        
    def __test_consecutive_process(self, input_, expected):
        processed = self.module

        for i in range(0, len(expected)):
            processed, value = process(processed, input_[i])
            self.assertEquals(value, expected[i])

if __name__ == "__main__":
    main()