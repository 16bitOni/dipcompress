#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <stdlib.h>

#define WINDOW_SIZE 4096
#define LOOKAHEAD   18

/*
 * Core LZ77 encode — identical algorithm to lz77.py.
 * Output: raw token stream, 4 bytes per token:
 *   [distance_hi, distance_lo, length, next_byte]
 * Literals have distance=0 and length=0.
 * Returns number of bytes written.
 */
static int
_lz77_encode(const uint8_t *input, int input_len,
             uint8_t *output, int output_max)
{
    int pos = 0, out_pos = 0;

    while (pos < input_len) {
        int wstart = pos - WINDOW_SIZE;
        if (wstart < 0) wstart = 0;

        int lend = pos + LOOKAHEAD;
        if (lend > input_len) lend = input_len;
        int llen = lend - pos;

        int best_dist = 0, best_len = 0;

        for (int i = wstart; i < pos; i++) {
            int ml = 0;
            while (ml < llen && i + ml < pos && input[i + ml] == input[pos + ml])
                ml++;
            if (ml > best_len) {
                best_len  = ml;
                best_dist = pos - i;
            }
        }

        if (best_len >= 3) {
            int np = pos + best_len;
            if (np >= input_len) { best_len--; np--; }

            output[out_pos++] = (best_dist >> 8) & 0xFF;
            output[out_pos++] =  best_dist       & 0xFF;
            output[out_pos++] = (uint8_t)best_len;
            output[out_pos++] = input[np];
            pos += best_len + 1;
        } else {
            output[out_pos++] = 0;
            output[out_pos++] = 0;
            output[out_pos++] = 0;
            output[out_pos++] = input[pos];
            pos++;
        }
    }
    return out_pos;
}

/* ── Python wrapper ───────────────────────────────────────────────────── */

static PyObject *
py_lz77_encode(PyObject *self, PyObject *args)
{
    const uint8_t *input;
    Py_ssize_t input_len;

    if (!PyArg_ParseTuple(args, "y#", &input, &input_len))
        return NULL;

    int output_max = (int)input_len * 4 + 4;
    uint8_t *output = (uint8_t *)malloc(output_max);
    if (!output)
        return PyErr_NoMemory();

    int n = _lz77_encode(input, (int)input_len, output, output_max);
    PyObject *result = PyBytes_FromStringAndSize((char *)output, n);
    free(output);
    return result;
}

static PyMethodDef lz77_methods[] = {
    {"lz77_encode", py_lz77_encode, METH_VARARGS,
     "lz77_encode(data: bytes) -> bytes  —  raw 4-byte-per-token stream"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef lz77_module = {
    PyModuleDef_HEAD_INIT, "lz77_cext", NULL, -1, lz77_methods
};

PyMODINIT_FUNC
PyInit_lz77_cext(void)
{
    return PyModule_Create(&lz77_module);
}
