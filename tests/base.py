STRING_INPUT = "test"
TUPLE_INPUT = ("one", "two", "three")

class ChannelTestCase():
    def test_single(self):
        output = self.channel.send(STRING_INPUT)

        self.assertEquals(output, self.expected_string_input)

    def test_single_list(self):
        output = self.channel.send((STRING_INPUT, ))

        self.assertEquals(output, self.expected_string_input)

    def test_multiple(self):
        output = self.channel.send(TUPLE_INPUT)

        self.assertEquals(output, self.expected_tuple_input)
        
    def test_generator(self):
        input_ = (c for c in TUPLE_INPUT)
        output = self.channel.send(input_)

        self.assertEquals(output, self.expected_tuple_input)
        
class NoInputTestCase(object):
    def test_no_input(self):
        self.assertRaises(TypeError, self.channel.send, None)

    def test_empty(self):
        output = self.channel.send("")
        self.assertEquals(output, self.expected_no_input)

    def test_empty_list(self):
        output = self.channel.send(())
        self.assertEquals(output, self.expected_no_input)

class RepetitionTestCase(object):
    def test_repeated_send(self):
        for _ in range(5):
            output = self.channel.send(TUPLE_INPUT)
            self.assertEquals(output, self.expected_tuple_input)

    def test_consecutive_send(self):
        for _ in range(5):
            value = self.channel.send(TUPLE_INPUT)
            self.assertEquals(value, self.expected_tuple_input)

