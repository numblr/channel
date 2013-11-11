from modular.modules.base import process

STRING_INPUT = "test"
TUPLE_INPUT = ("one", "two", "three")

class ModuleTestCase():
    def test_single(self):
        output = self.module.process(STRING_INPUT).get_output()

        self.assertEquals(output, self.expected_string_input)

    def test_single_list(self):
        output = self.module.process((STRING_INPUT, )).get_output()

        self.assertEquals(output, self.expected_string_input)

    def test_multiple(self):
        output = self.module.process(TUPLE_INPUT).get_output()

        self.assertEquals(output, self.expected_tuple_input)
        
    def test_repeated_process(self):
        for _ in range(5):
            self.test_multiple()

    def test_generator(self):
        input_ = (c for c in TUPLE_INPUT)
        output = self.module.process(input_).get_output()

        self.assertEquals(output, self.expected_tuple_input)
        
class NoInputTestCase(object):
    def test_no_input(self):
        self.assertRaises(TypeError, self.module.process, None)

    def test_empty(self):
        output = self.module.process("").get_output()
        self.assertEquals(output, self.expected_no_input)

    def test_empty_list(self):
        output = self.module.process(()).get_output()
        self.assertEquals(output, self.expected_no_input)

class RepetitionTestCase(object):
    def test_repeated_process(self):
        for _ in range(5):
            output = self.module.process(TUPLE_INPUT).get_output()
            self.assertEquals(output, self.expected_tuple_input)

    def test_consecutive_process(self):
        processed = self.module
        for _ in range(5):
            processed, value = process(processed, TUPLE_INPUT)
            self.assertEquals(value, self.expected_tuple_input)

