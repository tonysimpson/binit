#include <Python.h>


typedef struct {
    PyObject_HEAD
    PyObject *name;
    PyObject *type;    
} Field;


typedef struct {
    long do_while_times;
    char *program_start;
    PyObject *value;
    Py_ssize_t store_pos;
} Frame;


#define CUR_FRAME (frames[frame_index])
#define PREV_FRAME (frames[frame_index - 1])
#define END_BLOCK 1
#define NEW_TUPLE 2
#define CAST      3
#define INT64     4
#define REPEAT    5

static PyObject * _frame_parser(char *buffer, long max_frames, char *program,  PyObject *type_callables) {
    Frame frames[max_frames];
    long frame_index = 0;
    CUR_FRAME.do_while_times = 0;
    CUR_FRAME.program_start = program;
    CUR_FRAME.value = NULL;
    CUR_FRAME.store_pos = 0;
    while (1) { /*eval loop */
        do { /* outer frame loops */
            while (1) { /* inner blocks */
                switch (*program++) {
                    case END_BLOCK:
                        goto end_block;
                    case NEW_TUPLE:
                        CUR_FRAME.value = PyTuple_New(*(Py_ssize_t*)program);
                        program += sizeof(Py_ssize_t);
                        CUR_FRAME.store_pos = 0;
                        break;
                    case CAST:
                        {
                            Py_ssize_t index = *(Py_ssize_t*)program;
                            program += sizeof(Py_ssize_t);
                            PyObject *callable = PyTuple_GET_ITEM(type_callables, index);

                            PyObject *new_value = PyObject_CallObject(callable, CUR_FRAME.value);
                            Py_DECREF(CUR_FRAME.value);
                            CUR_FRAME.value = new_value;
                        }
                        break;
                    case INT64:
                        {
                            PyTuple_SET_ITEM(CUR_FRAME.value, CUR_FRAME.store_pos++, _PyLong_FromByteArray(buffer, sizeof(long),  1, 1));
                            buffer += sizeof(long);
                        }
                        break;
                    case REPEAT:
                        {
                            long times = *(long*)program;
                            program += sizeof(long);
                            CUR_FRAME.value = PyTuple_New(times);
                            CUR_FRAME.store_pos = 0;
                            frame_index++;
                            CUR_FRAME.program_start = program;
                            CUR_FRAME.do_while_times = times - 1; /* we always loop once */
                            CUR_FRAME.value = NULL;
                            CUR_FRAME.store_pos = 0;
                        }
                        break;
                }
            }
end_block:
            if (frame_index == 0) {
                return CUR_FRAME.value;
            }
            else {
                PyTuple_SET_ITEM(PREV_FRAME.value, PREV_FRAME.store_pos++, CUR_FRAME.value);
                if(CUR_FRAME.do_while_times) {
                    program = CUR_FRAME.program_start; /* reset program to start of block */
                }
            }
        } while (CUR_FRAME.do_while_times--);
        frame_index--;
    }
}


static PyObject * parse(PyObject *module, PyObject *args)
{
    char *buffer;
    char *program;
    Py_ssize_t buffer_len;
    Py_ssize_t program_len;
    long max_frames;

    PyObject *type_callables;

    if (!PyArg_ParseTuple(args, "s#ls#O", &buffer, &buffer_len, &max_frames, &program, &program_len, &type_callables))
        return NULL;
    return _frame_parser(buffer, max_frames, program, type_callables);
}


static PyMethodDef _binit_functions[] = {
    {"parse", parse, METH_VARARGS, "parse"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _binit_module = {
    PyModuleDef_HEAD_INIT,
    "_binit",
    "C part of binit.",
    0,
    _binit_functions
};

PyMODINIT_FUNC
PyInit__binit(void)
{
    PyObject *m;
    m = PyModule_Create(&_binit_module);
    return m;
}
