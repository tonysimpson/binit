import construct
import struct

_struct = construct.Struct(
    'a' / construct.Int64sl,
    'b' / construct.Int64sl,
    'c' / construct.Int64sl)
format = construct.Array(10000, _struct)
format.build([{'a': 100, 'b': 100, 'c': 100}] * 10000)



"""

raw_get
raw_set
len


vector(intn, intn)
array(2, array(3, intn))
collection(intn, intn, intn)
struct(field('terry', intn), field('bobby', intn))
choice(
"""

class array:
    def __init__(self, item_count, item_type):
        self.item_count = item_count
        self.item_type = item_count

    def ___compiler(self):
        return [REPEAT] + self.item_type.___compile() + [TIMES(self.item_count), BUILD(list)]


class test_struct(object):
    __slots__ = ('a', 'b', 'c')
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return 'test_struct(a={!r}, b={!r}, c={!r})'.format(self.a, self.b, self.c)


def test(bytes):
    i = 0
    result = []
    format = struct.Struct('QQQ')
    pos = 0
    format_size = format.size
    while i < 10000:
        result.append(test_struct(*format.unpack_from(bytes, pos)))
        pos += format_size
        i += 1
    return result

    
a = format.build([{'a': 100, 'b': 100, 'c': 100}] * 10000)

import _binit

