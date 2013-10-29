Difference between _, __ and __xx__ in Python

16 Sep 2010

When learning Python many people don't really understand why so much underlines in the beginning of the methods, sometimes even in the end like __this__! I've already had to explain it so many times, it's time to document it.

One underline in the beginning
Python doesn't have real private methods, so one underline in the beginning of a method or attribute means you shouldn't access this method, because it's not part of the API. It's very common when using properties:

class BaseForm(StrAndUnicode):
    ...
    
    def _get_errors(self):
        "Returns an ErrorDict for the data provided for the form"
        if self._errors is None:
            self.full_clean()
        return self._errors
    
    errors = property(_get_errors)
This snippet was taken from django source code (django/forms/forms.py). This means errors is a property, and it's part of the API, but the method this property calls, _get_errors, is "private", so you shouldn't access it.

Two underlines in the beginning
This one causes a lot of confusion. It should not be used to mark a method as private, the goal here is to avoid your method to be overridden by a subclass. Let's see an example:

class A(object):
    def __method(self):
        print "I'm a method in A"
    
    def method(self):
        self.__method()
     
a = A()
a.method()
The output here is

$ python example.py 
I'm a method in A
Fine, as we expected. Now let's subclass A and customize __method

class B(A):
    def __method(self):
        print "I'm a method in B"

b = B()
b.method()
and now the output is...

$ python example.py
I'm a method in A
as you can see, A.method() didn't call B.__method() as we could expect. Actually this is the correct behavior for __. So when you create a method starting with __ you're saying that you don't want anybody to override it, it will be accessible just from inside the own class.

How python does it? Simple, it just renames the method. Take a look:

a = A()
a._A__method()  # never use this!! please!
$ python example.py
I'm a method in A
If you try to access a.__method() it won't work either, as I said, __method is just accessible inside the class itself.
