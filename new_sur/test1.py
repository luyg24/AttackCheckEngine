class Test(object):
    def __init__(self, data):
        self.data = data
    def check(self):
        return self.data
    def execute(self):
        check = self.check()
        print 'I m execute'
        print check

a = Test('hello')
a.execute()