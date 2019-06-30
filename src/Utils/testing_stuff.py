class A():
    def __init__(self, a):
        self.a = a

class B(A):
    def __init__(self,b,_):
        super().__init__(None)
        self.b = b

b = B(1,2)
print(b.a)