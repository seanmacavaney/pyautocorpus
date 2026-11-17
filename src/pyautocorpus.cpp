#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "pcre.h"
#include "Textifier.h"
#include <iostream>
#include "utilities.h"


typedef struct {
    PyObject_HEAD
    Textifier *textifier;
} TextifierObject;

static void
Textifier_dealloc(TextifierObject *self)
{
  delete self->textifier;
  PyTypeObject *tp = Py_TYPE(self);
  freefunc tp_free = (freefunc)PyType_GetSlot(tp, Py_tp_free);
  tp_free(self);
  Py_DECREF(tp); // heap type instances hold a reference to their type
}

static PyObject *
Textifier_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    TextifierObject *self;

    self = (TextifierObject *)((allocfunc)PyType_GetSlot(type, Py_tp_alloc))(type, 0);
    if (self != NULL) {
        self->textifier = NULL;
    }

    return (PyObject *)self;
}

static int
Textifier_init(TextifierObject *self, PyObject *args, PyObject *kwds)
{
    delete self->textifier;
    self->textifier = new Textifier();
    return 0;
}

static PyObject *Textifier_textify(TextifierObject* self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"input", NULL};
    PyObject *input = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &input)) {
        return NULL;
    }

    if (!PyUnicode_Check(input)) {
        PyErr_SetString(PyExc_RuntimeError, "Input must be a string");
        return NULL;
    }

    // PyUnicode_AsUTF8AndSize is only in the limited API from 3.10, so go via bytes
    PyObject* input_bytes = PyUnicode_AsUTF8String(input);
    if (input_bytes == NULL) {
        return NULL;
    }
    Py_ssize_t len;
    char* input_chars;
    if (PyBytes_AsStringAndSize(input_bytes, &input_chars, &len) < 0) {
        Py_DECREF(input_bytes);
        return NULL;
    }

    char* output_chars = new char[2*len+1]; // not sure why it needs to be so big (2*l+1), but matches the command line version

    PyObject* output = NULL;

    try {
      int output_len = self->textifier->textify(input_chars, len, output_chars, len);
      output_chars[output_len] = '\0'; // terminate string

      output = PyUnicode_FromFormat("%s", output_chars);
    } catch (Error ex) {
        PyObject* err = Py_BuildValue("(si)", ex.message.c_str(), ex.pos);
        PyErr_SetObject(PyExc_ValueError, err);
        Py_DECREF(err); // now owned by PyErr
    }

    delete[] output_chars;
    Py_DECREF(input_bytes);
    return output;
}

static PyMethodDef Textifier_methods[] = {
    {"textify", (PyCFunction) Textifier_textify, METH_VARARGS | METH_KEYWORDS,
     "Remove wiki markup from text"},
    {NULL}  /* Sentinel */
};

static PyType_Slot Textifier_slots[] = {
    {Py_tp_dealloc, (void *) Textifier_dealloc},
    {Py_tp_doc, (void *) "autocorpus wikipedia textifier"},
    {Py_tp_methods, (void *) Textifier_methods},
    {Py_tp_init, (void *) Textifier_init},
    {Py_tp_new, (void *) Textifier_new},
    {0, NULL}
};

static PyType_Spec Textifier_spec = {
    "pyautocorpus.Textifier",
    sizeof(TextifierObject),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    Textifier_slots
};

static PyMethodDef PyAutoCorpusMethods[] = {
    {NULL, NULL, 0, NULL}
};

static PyModuleDef pyautocorpus_module = {
    PyModuleDef_HEAD_INIT,
    "pyautocorpus",
    "c++ extensions for AutoCorpus",
    -1,
    PyAutoCorpusMethods
};

PyMODINIT_FUNC
PyInit_pyautocorpus(void)
{
    PyObject *m;

    m = PyModule_Create(&pyautocorpus_module);
    if (m == NULL)
        return NULL;

    PyObject *textifier_type = PyType_FromSpec(&Textifier_spec);
    if (textifier_type == NULL) {
      Py_DECREF(m);
      return NULL;
    }

    // PyModule_AddObject steals the reference on success only
    if (PyModule_AddObject(m, "Textifier", textifier_type) < 0) {
      Py_DECREF(textifier_type);
      Py_DECREF(m);
      return NULL;
    }

    return m;
}
