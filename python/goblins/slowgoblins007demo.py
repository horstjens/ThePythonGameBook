__author__ = 'Horst JENS'
# see http://ThePythonGameBook.com

def output(a,b=20,c=30):
    """a docstring in triple quotes explaining that this function print out variables"""
    print("inside the function. The parameters a,b,c:")
    print("a: {} b: {} c: {}".format(a,b,c))
    print("i set now d locally to -100")
    d = -100 # a local d
    print("the local variable d: {}".format(d))
    print("i manipulate locally a and double it")
    a *= 2 # the same as a = a * 2
    print("local a is now: {}".format(a))
    print("returning a,b and c")
    return a,b,c

# calling the function
a = 5
b = 22
c = 100
d = 5000

print("a,b,c,d:",a,b,c,d)
a,b,c = output(a)
print("a,b,c,d:",a,b,c,d)
print(output.__doc__)