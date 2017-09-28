def a(i):
    print 'a', i

def b(i):
    if i == 4:
        return()
    else:
        a(i)

def c():
    for i in range(10):
        b(i)

c()