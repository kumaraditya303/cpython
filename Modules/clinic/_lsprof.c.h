/*[clinic input]
preserve
[clinic start generated code]*/

#ifdef Py_BUILD_CORE
#include "pycore_gc.h"            // PyGC_Head
#include "pycore_runtime.h"       // _Py_ID()
#endif


PyDoc_STRVAR(_lsprof_Profiler_getstats__doc__,
"getstats($self, /)\n"
"--\n"
"\n"
"list of profiler_entry objects.\n"
"\n"
"getstats() -> list of profiler_entry objects\n"
"\n"
"Return all information collected by the profiler.\n"
"Each profiler_entry is a tuple-like object with the\n"
"following attributes:\n"
"\n"
"    code          code object\n"
"    callcount     how many times this was called\n"
"    reccallcount  how many times called recursively\n"
"    totaltime     total time in this entry\n"
"    inlinetime    inline time in this entry (not in subcalls)\n"
"    calls         details of the calls\n"
"\n"
"The calls attribute is either None or a list of\n"
"profiler_subentry objects:\n"
"\n"
"    code          called code object\n"
"    callcount     how many times this is called\n"
"    reccallcount  how many times this is called recursively\n"
"    totaltime     total time spent in this call\n"
"    inlinetime    inline time (not in further subcalls)");

#define _LSPROF_PROFILER_GETSTATS_METHODDEF    \
    {"getstats", (PyCFunction)(void(*)(void))_lsprof_Profiler_getstats, METH_METHOD|METH_FASTCALL|METH_KEYWORDS, _lsprof_Profiler_getstats__doc__},

static PyObject *
_lsprof_Profiler_getstats_impl(ProfilerObject *self, PyTypeObject *cls);

static PyObject *
_lsprof_Profiler_getstats(ProfilerObject *self, PyTypeObject *cls, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
    #define NUM_KEYWORDS 0
    #if NUM_KEYWORDS == 0

    #  ifdef Py_BUILD_CORE
    #    define KWTUPLE (PyObject *)&_Py_SINGLETON(tuple_empty)
    #  else
    #    define KWTUPLE NULL
    #  endif

    #else  // NUM_KEYWORDS != 0
    #  ifdef Py_BUILD_CORE

    static struct {
        PyObject_VAR_HEAD
        PyObject *ob_item[NUM_KEYWORDS];
    } _kwtuple = {
        .ob_base = PyVarObject_HEAD_INIT(&PyTuple_Type, NUM_KEYWORDS)
        .ob_item = {  },
    };
    #  define KWTUPLE ((PyObject *)(&_kwtuple))

    #  else  // !Py_BUILD_CORE
    #    define KWTUPLE NULL
    #  endif  // !Py_BUILD_CORE
    #endif  // NUM_KEYWORDS != 0
    #undef NUM_KEYWORDS

    static const char * const _keywords[] = { NULL};
    static _PyArg_Parser _parser = {
        .keywords = _keywords,
        .format = ":getstats",
        .kwtuple = KWTUPLE,
    };
    #undef KWTUPLE

    if (!_PyArg_ParseStackAndKeywords(args, nargs, kwnames, &_parser
        )) {
        goto exit;
    }
    return_value = _lsprof_Profiler_getstats_impl(self, cls);

exit:
    return return_value;
}
/*[clinic end generated code: output=0826423995b6660b input=a9049054013a1b77]*/
