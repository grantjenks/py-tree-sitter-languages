#include <Python.h>

typedef struct TSLanguage TSLanguage;

#ifndef TS_LANGUAGE_NAME
#error TS_LANGUAGE_NAME must be defined
#endif

#define _str(s) #s
#define str(s) _str(s)
#define _cat(a, b) a##b
#define cat(a, b) _cat(a, b)

#define TS_LANGUAGE_FUNC cat(tree_sitter_, TS_LANGUAGE_NAME)
#define TS_LANGUAGE_METHOD cat(TS_LANGUAGE_NAME, _language)
#define TS_LANGUAGE_MODULE cat(PyInit_, TS_LANGUAGE_NAME)

TSLanguage *TS_LANGUAGE_FUNC(void);

static PyObject* TS_LANGUAGE_METHOD(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(args)) {
    return PyLong_FromVoidPtr(TS_LANGUAGE_FUNC());
}

static PyMethodDef methods[] = {
    {"language", TS_LANGUAGE_METHOD, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = str(TS_LANGUAGE_NAME),
    .m_doc = NULL,
    .m_size = -1,
    .m_methods = methods
};

PyMODINIT_FUNC TS_LANGUAGE_MODULE(void) {
    return PyModule_Create(&module);
}
