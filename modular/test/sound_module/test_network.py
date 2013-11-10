from modular.sound_module.modules import process, Delay, Reverse, Sum
from modular.sound_module.network import Network, NetworkDefinition, UndefinedValueError,\
    NameConflictError, IllegalOrderError, NetworkFactory
from unittest import TestCase, main

MODULES = (("a", Sum()), ("b", Reverse()), ("c", Delay()))
CONNECTIONS = {"b": "a", "c": "b"} 

class NetworkDefinitionTestCase(TestCase):
    def setUp(self):
        self.definition = NetworkDefinition(("typeone", "typetwo"))
        
    def test_add_module(self):
        self.definition.add_module("test", "typeone")
        
        self.assertEquals(self.definition.available_modules_ids(), ["test"])

    def test_add_multiple_modules(self):
        self.__add_module_one_to_four()
        
        self.assertEquals(self.definition.available_modules_ids(), ["one", "two", "three", "four"])

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
        self.assertRaisesRegexp(UndefinedValueError, "other", self.definition.add_module, "test", "other")

    def test_conflicting_module_name(self):
        self.definition.add_module("test", "typeone")

        self.assertRaisesRegexp(NameConflictError, "test", self.definition.add_module, "test", "typetwo")

    def test_invalid_module_order(self):
        self.definition.add_module("one", "typeone")
        self.definition.add_module("two", "typetwo")
        
        self.assertRaisesRegexp(IllegalOrderError, "two must have been defined before one", self.definition.add_connection, "two", "one")
        
    def test_invalid_module_name_in_connection(self):
        self.definition.add_module("one", "typeone")
        self.definition.add_module("two", "typetwo")
        
        self.assertRaisesRegexp(UndefinedValueError, "three", self.definition.add_connection, "one", "three")
        self.assertRaisesRegexp(UndefinedValueError, "three", self.definition.add_connection, "three", "two")
        
        
TEST_FACTORIES = {"sum": Sum.create, "reverse": Reverse.create}

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
        self.assertItemsEqual(self.factory.available_module_types(), ("sum", "reverse"))
        
    def test_create(self):
        network = self.factory.create(TEST_DEFINITION)
        output = network.process("test").get_output()
        
        self.assertEquals(output, "tset")
        
    def test_define(self):
        self.factory.define_module_type("test", TEST_DEFINITION)
        
        self.assertItemsEqual(self.factory.available_module_types(), ("sum", "reverse", "test"))
        
    def test_define_and_use(self):
        self.factory.define_module_type("test", TEST_DEFINITION)
        
        definition = NetworkDefinition(self.factory.available_module_types())
        definition.add_module("test", "test")
        
        test_network = self.factory.create(definition)
        
        output = test_network.process("test").get_output()
        
        self.assertEquals(output, "tset")
        
    def test_define_with_name_conflict(self):
        self.assertRaisesRegexp(NameConflictError, "sum", self.factory.define_module_type, "sum", TEST_DEFINITION)
        
class NetworkTestCase(TestCase):
    def setUp(self):
        self.module = Network(MODULES, CONNECTIONS)
        
    def test_empty(self):
        empty_network = NetworkFactory().create(NetworkDefinition([]))
        
        self.assertEquals(empty_network.process("test").get_output(), "")
        
    def test_consecutive_process(self):
        input_ = ("hello", "world", "", "", "", "")
        expected = (Delay.INITIAL_VALUE, "olleh", "dlrow", "", "")
        
        processed = self.module

        for i in range(0, len(expected)):
            processed, value = process(processed, input_[i])
            self.assertEquals(value, expected[i])

if __name__ == "__main__":
    main()