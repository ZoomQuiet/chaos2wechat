import pyfsm
from pyfsm import state, transition

@state('say_hello')
@transition('goodbye', 'goodbye')
def meet_and_greet(self):
    print 'hello, world!'
    @self.callback('hi')
    def print_hello(event):
        print 'hello, again'

@state('say_hello')
def goodbye(self):
    print 'leaving so soon?'

say_hello = pyfsm.Registry.get_task('say_hello')
say_hello.start('meet_and_greet')
say_hello.send('hi')
say_hello.send('dead message')
#say_hello.send('hi')
say_hello.send('goodbye')

'''
seek->list->reg->conf->bye
'''
@state('my_reg')
@transition('end', 'end')
@transition('r', 'reg')
def seek(self):
    print 'seek crt. events...'
    @self.callback('l')
    def list(event):
        print 'list events:...'

@state('my_reg')
@transition('c', 'conf')
def reg(self):
    print 'reg some one event?!'

@state('my_reg')
@transition('b', 'bye')
def conf(self):
    print 'confirmed reg the event!'

@state('my_reg')
def bye(self):
    print 'bye and c u there!'

@state('my_reg')
def end(self):
    print 'broken flow!'

my_reg = pyfsm.Registry.get_task('my_reg')
my_reg.start('seek')
#my_reg.send('end')
my_reg.send('l')
my_reg.send('r')
#my_reg.send('c')
my_reg.send('b')

print "\tOTHER SFM matter..."
crt_reg = pyfsm.Registry.get_task('my_reg')
my_reg.start('reg')
my_reg.send('c')
