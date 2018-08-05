from binit import *

def test_compiler():
    d = array(10000, struct(field('a', int64), field('b', int64), field('c', int64)))
    p = Parser()
    p._compile(d, 1)
