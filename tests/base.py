class ChannelTestCase():
    def test_single(self):
        output = self.channel.send(self.single_input)

        self.assertEqual(output, self.expected_single_input)

    def test_single_list(self):
        output = self.channel.send((self.single_input, ))

        self.assertEqual(output, self.expected_single_input)

    def test_multiple(self):
        output = self.channel.send(self.tuple_input)

        self.assertEqual(output, self.expected_tuple_input)
        
    def test_generator(self):
        input_ = (c for c in self.tuple_input)
        output = self.channel.send(input_)

        self.assertEqual(output, self.expected_tuple_input)
        
class NoInputTestCase(object):
    def test_no_input(self):
        self.assertRaises(TypeError, self.channel.send, None)

    def test_empty(self):
        output = self.channel.send("")
        self.assertEqual(output, self.expected_no_input)

    def test_empty_list(self):
        output = self.channel.send(())
        self.assertEqual(output, self.expected_no_input)

class MemorylessTestCase(object):
    def test_repeated_send(self):
        for i in range(5):
            output = self.channel.send(self.tuple_input)
            self.assertEqual(output, self.expected_tuple_input, "Failed at {0}".format(i))

    def test_consecutive_send(self):
        for i in range(5):
            value = self.channel.send(self.tuple_input)
            self.assertEqual(value, self.expected_tuple_input, "Failed at {0}".format(i))

