from itertools import islice
from .._module import Module
from .._network import network_channel
from ..network import NetworkDefinition, UndefinedNameError, \
    NameConflictError, IllegalOrderError, NetworkFactory
from ..string_channels import DELAY_INITIAL, sum_channel, \
    reverse_channel, delay_channel, process_sequence
from ..channels.base import ChannelTestCase, NoInputTestCase
from unittest import TestCase, main

class NetworkDefinitionTestCase(TestCase):
    def setUp(self):
        self.definition = NetworkDefinition(("typeone", "typetwo"))
        
    def test_add_module(self):
        self.definition.add_module("test", "typeone")
        
        self.assertEquals(self.definition.available_module_ids(), ["test"])

    def test_add_multiple_modules(self):
        self.__add_module_one_to_four()
        
        self.assertEquals(self.definition.available_module_ids(), ["one", "two", "three", "four"])

    def test_add_connections(self):
        self.__add_module_one_to_four()
        
        self.definition.add_connection("one", "two")
        self.definition.add_connection("two", "three")
        self.definition.add_connection("three", "four")
        self.definition.add_connection("one", "four")
        
        expected_modules = (Module("one", "typeone"),
                            Module("two", "typetwo"),
                            Module("three", "typetwo"),
                            Module("four", "typeone"))
        
        expected_connections = {"two": ("one", ),
                                "three": ("two", ),
                                "four": ("three", "one")}
        
        actual_modules, actual_connections = self.definition._get_state()

        self.assertEquals(actual_modules, expected_modules)
        self.assertDictEqual(actual_connections, expected_connections)
        
    def __add_module_one_to_four(self):
        self.definition.add_module("one", "typeone")
        self.definition.add_module("two", "typetwo")
        self.definition.add_module("three", "typetwo")
        self.definition.add_module("four", "typeone")
        
    def test_invalid_channel_type(self):
        self.assertRaisesRegexp(UndefinedNameError, "other", self.definition.add_module, "test", "other")

    def test_conflicting_module_name(self):
        self.definition.add_module("test", "typeone")

        self.assertRaisesRegexp(NameConflictError, "test", self.definition.add_module, "test", "typetwo")

    def test_invalid_module_order(self):
        self.__add_module_one_to_four()
        
        self.assertRaisesRegexp(IllegalOrderError, "\"two\" must have been defined before \"one\"", self.definition.add_connection, "two", "one")
        
    def test_invalid_module_name_in_connection(self):
        self.__add_module_one_to_four()
        
        self.assertRaisesRegexp(UndefinedNameError, "five", self.definition.add_connection, "one", "five")
        self.assertRaisesRegexp(UndefinedNameError, "five", self.definition.add_connection, "five", "two")
        
    def test_duplicate_connection(self):
        self.__add_module_one_to_four()
        self.definition.add_connection("one", "two")
        
        self.assertRaisesRegexp(NameConflictError, "\"one\" is already connected to \"two\"", self.definition.add_connection, "one", "two")
        
TEST_CHANNELS = {"sum": sum_channel, "reverse": reverse_channel, "delay": delay_channel}

def create_test_definition(channel_types):
    definition = NetworkDefinition(channel_types)
    definition.add_module("one", "sum")
    definition.add_module("two", "reverse")
    
    definition.add_connection("one", "two")
    
    return definition

TEST_DEFINITION = create_test_definition(TEST_CHANNELS.keys())
        
class NetworkFactoryTestCase(TestCase):
    def setUp(self):
        self.factory = NetworkFactory(TEST_CHANNELS.copy())
        
    def test_available_types(self):
        self.assertItemsEqual(self.factory.available_channel_types(), ("sum", "reverse", "delay"))
        
    def test_create(self):
        test_network = self.factory.create(TEST_DEFINITION)()
        output = test_network.send("test")
        
        self.assertEquals(output, "tset")
        
    def test_define(self):
        self.factory.define_channel_type("test", TEST_DEFINITION)
        
        self.assertItemsEqual(self.factory.available_channel_types(), ("sum", "reverse", "delay", "test"))
        
    def test_define_and_use(self):
        self.factory.define_channel_type("test", TEST_DEFINITION)
        
        definition = NetworkDefinition(self.factory.available_channel_types())
        definition.add_module("test", "test")
        
        test_network = self.factory.create(definition)()
        
        output = test_network.send("test")
        
        self.assertEquals(output, "tset")
        
    def test_create_independent(self):
        output_1 = self.__create_and_process_delay(self.factory)
        output_2 = self.__create_and_process_delay(self.factory)
        
        self.assertEquals(output_1, DELAY_INITIAL)
        self.assertEquals(output_2, DELAY_INITIAL)
        
    def test_create_and_start_multiple_times(self):
        test_channel = self.__create_delay(self.factory)
        
        for i in range(5):
            outputs = process_sequence(test_channel(), ("test", ))

            self.assertEquals(tuple(islice(outputs, 3)), (DELAY_INITIAL, "test", ""), "Failed at {0}".format(i))
        
    def __create_delay(self, factory):    
        definition = NetworkDefinition(self.factory.available_channel_types())
        definition.add_module("test", "delay")
        
        return factory.create(definition)
    
    def __create_and_process_delay(self, factory):
        definition = NetworkDefinition(self.factory.available_channel_types())
        definition.add_module("test", "delay")
        
        test_network = self.__create_delay(factory)()
        
        return test_network.send("test")
        
    def test_define_with_name_conflict(self):
        self.assertRaisesRegexp(NameConflictError, "sum", self.factory.define_channel_type, "sum", TEST_DEFINITION)
        
MODULES = (Module("a", sum_channel), Module("b", reverse_channel), Module("c", delay_channel))
CONNECTIONS = {"b": "a", "c": "b"}
INCOMPLETE_CONNECTIONS = {"b": "a"}

class NetworkTestCase(TestCase, ChannelTestCase, NoInputTestCase):
    def setUp(self):
        self.channel = network_channel(MODULES, CONNECTIONS.copy())
        self.expected_string_input = DELAY_INITIAL
        self.expected_tuple_input = DELAY_INITIAL
        self.expected_no_input = DELAY_INITIAL
        
    def test_empty(self):
        empty_network = NetworkFactory({}).create(NetworkDefinition([]))()
        
        self.assertEquals(empty_network.send("test"), None)
        
    def test_consecutive_process(self):
        input_ = ("hello", "world", "", "", "", "")
        expected = (DELAY_INITIAL, "olleh", "dlrow", "", "")
        
        self.__assert_processed(self.channel, input_, expected)
        
    def test_no_path_to_output(self):
        net = network_channel(MODULES, INCOMPLETE_CONNECTIONS.copy())

        input_ = ("hello", "world", "", "", "", "")
        expected = (DELAY_INITIAL, "", "", "", "")
        
        self.__assert_processed(net, input_, expected)
        
    def test_multiple_calls_to_channel_function(self):
        for _ in range(5):
            self.test_no_path_to_output()
        
    def __assert_processed(self, network, input_, expected):
        for i in range(0, len(expected)):
            value = network.send(input_[i])
            self.assertEquals(value, expected[i])

if __name__ == "__main__":
    main()