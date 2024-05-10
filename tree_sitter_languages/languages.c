#include "./languages.h"

TS_LANGUAGE_INIT(dot)
TS_LANGUAGE_INIT(elisp)
TS_LANGUAGE_INIT(elm)
TS_LANGUAGE_INIT(fixed_form_fortran)
TS_LANGUAGE_INIT(fortran)
TS_LANGUAGE_INIT(gomod)
TS_LANGUAGE_INIT(hack)
TS_LANGUAGE_INIT(hcl)
TS_LANGUAGE_INIT(kotlin)
TS_LANGUAGE_INIT(make)
TS_LANGUAGE_INIT(objc)
TS_LANGUAGE_INIT(rst)
TS_LANGUAGE_INIT(scala)
TS_LANGUAGE_INIT(sql)
TS_LANGUAGE_INIT(terraform)

static PyMethodDef methods[] = {
    TS_LANGUAGE_METHOD(dot),
    TS_LANGUAGE_METHOD(elisp),
    TS_LANGUAGE_METHOD(elm),
    TS_LANGUAGE_METHOD(fixed_form_fortran),
    TS_LANGUAGE_METHOD(fortran),
    TS_LANGUAGE_METHOD(gomod),
    TS_LANGUAGE_METHOD(hack),
    TS_LANGUAGE_METHOD(hcl),
    TS_LANGUAGE_METHOD(kotlin),
    TS_LANGUAGE_METHOD(make),
    TS_LANGUAGE_METHOD(objc),
    TS_LANGUAGE_METHOD(rst),
    TS_LANGUAGE_METHOD(scala),
    TS_LANGUAGE_METHOD(sql),
    TS_LANGUAGE_METHOD(terraform),
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "languages",
    .m_doc = NULL,
    .m_size = -1,
    .m_methods = methods
};

PyMODINIT_FUNC PyInit_languages(void) {
    return PyModule_Create(&module);
}
