

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
        exec class_def in namespace
        self.instance_constructor = namespace['struct_instance']


class array:
    __slots__ = ('length', 'type')

    def __init__(self, length, type):
        self.length = length
        self.type = type

    def __repr__(self):
        return 'array(length={!r}, type={!r})'.format(self.length, self.type)






