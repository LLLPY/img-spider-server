
class A:
    pass

class B(A):
    pass

b = B()
print(isinstance(b,A))