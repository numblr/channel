from modular.channels.channels import sum_channel, init_channel, identity, \
    memoryless_channel

if __name__ == '__main__':
    ch = init_channel(sum_channel)
    print "s", ch.send(("a", "b"))
    print "s", ch.send("v")
    print "s", ch.send("b")
    print "s", ch.send("sd")