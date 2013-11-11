from modular.modules.base import process, Sum
from modular.modules.network import Network, NetworkDefinition, \
    UndefinedNameError, NameConflictError, IllegalOrderError, NetworkFactory
from modular.modules.string_modules import Delay, Reverse
from modular.test.modules.base import ModuleTestCase, NoInputTestCase
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
        
        expected_modules = (("one", "typeone"),
                            ("two", "typetwo"),
                            ("three", "typetwo"),
                            ("four", "typeone"))
        
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
        
    def test_invalid_module_type(self):
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
        
TEST_FACTORIES = {"sum": Sum.create, "reverse": Reverse.create, "delay": Delay.create}

def create_test_definition(module_types):
    definition = NetworkDefinition(module_types)
    definition.add_module("one", "sum")
    definition.add_module("two", "reverse")
    
    definition.add_connection("one", "two")
    
    return definition

TEST_DEFINITION = create_test_definition(TEST_FACTORIES.keys())
        
class NetworkFactoryTestCase(TestCase):
    def setUp(self):
        self.factory = NetworkFactory(TEST_FACTORIES.copy())
        
    def test_available_types(self):
        self.assertItemsEqual(self.factory.available_module_types(), ("sum", "reverse", "delay"))
        
    def test_create(self):
        network = self.factory.create(TEST_DEFINITION)
        output = network.process("test").get_output()
        
        self.assertEquals(output, "tset")
        
    def test_define(self):
        self.factory.define_module_type("test", TEST_DEFINITION)
        
        self.assertItemsEqual(self.factory.available_module_types(), ("sum", "reverse", "delay", "test"))
        
    def test_define_and_use(self):
        self.factory.define_module_type("test", TEST_DEFINITION)
        
        definition = NetworkDefinition(self.factory.available_module_types())
        definition.add_module("test", "test")
        
        test_network = self.factory.create(definition)
        
        output = test_network.process("test").get_output()
        
        self.assertEquals(output, "tset")
        
    def test_create_independent(self):
        output_1 = self.__create_and_process_delay(self.factory)
        output_2 = self.__create_and_process_delay(self.factory)
        
        self.assertEquals(output_1, Delay.INITIAL_VALUE)
        self.assertEquals(output_2, Delay.INITIAL_VALUE)
        
    def __create_and_process_delay(self, factory):
        definition = NetworkDefinition(self.factory.available_module_types())
        definition.add_module("test", "delay")
        
        test_network = factory.create(definition)
        
        return test_network.process("test").get_output()
        
    def test_define_with_name_conflict(self):
        self.assertRaisesRegexp(NameConflictError, "sum", self.factory.define_module_type, "sum", TEST_DEFINITION)
        
MODULES = (("a", Sum()), ("b", Reverse()), ("c", Delay()))
CONNECTIONS = {"b": "a", "c": "b"}
INCOMPLETE_CONNECTIONS = {"b": "a"}

class NetworkTestCase(TestCase, ModuleTestCase, NoInputTestCase):
    def setUp(self):
        self.module = Network(MODULES, CONNECTIONS.copy())
        self.expected_string_input = Delay.INITIAL_VALUE
        self.expected_tuple_input = Delay.INITIAL_VALUE
        self.expected_no_input = Delay.INITIAL_VALUE
        
    def test_empty(self):
        empty_network = NetworkFactory({}).create(NetworkDefinition([]))
        
        self.assertEquals(empty_network.process("test").get_output(), "")
        
    def test_consecutive_process(self):
        input_ = ("hello", "world", "", "", "", "")
        expected = (Delay.INITIAL_VALUE, "olleh", "dlrow", "", "")
        
        processed = self.module

        for i in range(0, len(expected)):
            processed, value = process(processed, input_[i])
            self.assertEquals(value, expected[i])
        
    def test_unconnected_module(self):
        processed = Network(MODULES, INCOMPLETE_CONNECTIONS.copy())

        input_ = ("hello", "world", "", "", "", "")
        expected = (Delay.INITIAL_VALUE, "", "", "", "")
        
        for i in range(0, len(expected)):
            processed, value = process(processed, input_[i])
            self.assertEquals(value, expected[i])

if __name__ == "__main__":
    main()