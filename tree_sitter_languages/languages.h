#include <Python.h>

typedef struct TSLanguage TSLanguage;

#define _NL

#define _LANG_FUNC(name) tree_sitter_##name

#define _METHOD_FUNC(name) languages_##name

#define TS_LANGUAGE_INIT(name) \
    TSLanguage *_LANG_FUNC(name)(void); \
    \
    static PyObject *_METHOD_FUNC(name)(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(args)) { \
        return PyLong_FromVoidPtr(_LANG_FUNC(name)()); \
    }

#define TS_LANGUAGE_METHOD(name) { #name, _METHOD_FUNC(name), METH_NOARGS, NULL }
