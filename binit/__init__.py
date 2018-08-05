

#vector(intn, intn)
#array(2, array(3, intn))
#collection(intn, intn, intn)
#struct(field('terry', intn), field('bobby', intn))


class field:
    __slots__ = ('name', 'type')

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return 'field(name={!r}, type={!r})'.format(self.name, self.type)


def _struct_class_def(fields):
    class_def = []
    class_def.append('class struct_instance:\n')
    class_def.append('    __slots__ = (')
    class_def.append(', '.join(repr(field.name) for field in fields))
    class_def.append(', )\n')
    class_def.append('    def __init__(self, ')
    class_def.append(', '.join(field.name for field in fields))
    class_def.append('):\n')
    for field in fields:
        class_def.append('        self.{0} = {0}\n'.format(field.name))
    class_def.append('\n')
    class_def.append('    def __repr__(self):\n')
    class_def.append('        return "struct_instance(')
    class_def.append(', '.join('{}={{}}'.format(field.name)  for field in fields))
    class_def.append(')".format(')
    class_def.append(', '.join('self.{}'.format(field.name)  for field in fields))
    class_def.append(')\n\n')
    return ''.join(class_def)


class struct:
    __slots__ = ('fields', 'instance_constructor')

    def __init__(self, *fields):
        assert fields
        self.fields = fields
        namespace = {'__name__': 'binit'}
        class_def = _struct_class_def(fields)
        exec(class_def, namespace)
        self.instance_constructor = namespace['struct_instance']
    
    def __repr__(self):
        return 'struct({})'.format(
                ', '.join('{}={!r}'.format(
                        field.name, field.type
                    ) for field in self.fields
                )
            )

class array:
    __slots__ = ('length', 'type')

    def __init__(self, length, type):
        self.length = length
        self.type = type

    def __repr__(self):
        return 'array(length={!r}, type={!r})'.format(self.length, self.type)


class struct_format_type:
    __slots__ = ('name', 'format')

    def __init__(self, name, format):
        self.name = name
        self.format = format

    def __repr__(self):
        return '{}'.format(self.name)


int64 = struct_format_type('int64', 'q')

END = 0
REPEAT = 1
CALL = 2
FORMAT = 3


class frame:
    __slots__ = ('value', 'repeat', 'start_pos')

    def __init__(self, value, repeat, start_pos):
        self.value = value
        self.repeat = repeat
        self.start_pos = start_pos


class Parser:
    def __init__(self):
        self.max_frames = 0
        self.code = None
        self._formated_list = []

    def compiler(self, definition):
        self.code = self._compile(definition, 1)

    def _finish_formated(self):
        if self._formated_list:
            count = len(self._formated_list)
            code = ''.join(self._formated_list)
            del self._formated_list[:]
            return [FORMAT, count, code]
        return []

    def _compile(self, current, frame_depth):
        if frame_depth > self.max_frames:
            self.max_frames = frame_depth
        if type(current) == struct_format_type:
            self._formated_list.append(current.format)
            return []
        else:
            r = self._finish_formated()
        if type(current) == array:
            return r + [REPEAT, current.length] + self._compile(current.type, frame_depth + 1) + self._finish_formated() + [END]
        elif type(current) == struct:
            for f in current.fields:
                r += self._compile(f.type, frame_depth + 1)
            return r + self._finish_formated() + [CALL, current.instance_constructor, END]
    
    def parse(self, buffer):
        stack = [frame(None, 0) for i in range(self.max_frames)]
        stack_pos = 0
        stack[stack_pos].value = (,)
        code_pos = 0
        while True:
            op = self.code[code_pos]
            code_pos += 1
            if op == REPEAT:
                times = self.code[code_pos]
                code_pos += 1
                stack_pos += 1
                stack[stack_pos].value = (,)
                stack[stack_pos].start_pos = code_pos
                continue
            if stack[stack_pos].repeat:
                stack[stack_pos].repeat -= 1








