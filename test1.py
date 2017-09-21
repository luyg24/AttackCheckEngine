
def test():
    return test2()

def test2():
    return 1, 2, 3

a, b, c = test()
print a, b, c