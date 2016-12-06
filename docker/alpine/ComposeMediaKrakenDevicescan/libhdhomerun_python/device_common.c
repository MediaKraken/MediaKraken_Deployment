/*
 * device_common.c
 *
 * Copyright © 2015 Michael Mohr <akihana@gmail.com>.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 3.0 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301 USA.
 */

#include "device_common.h"

/* String constants for use when raising exceptions */
const char * const DEVICE_ERR_REJECTED_OP = "the operation was rejected";
const char * const DEVICE_ERR_COMMUNICATION = "communication error sending request to hdhomerun device";
const char * const DEVICE_ERR_UNDOCUMENTED = "undocumented error reported by library";

/* Internal */
PyObject *build_tuner_status_dict(struct hdhomerun_tuner_status_t *status) {
    PyObject *rv, *dv;

    rv = PyDict_New();
    if(!rv) return NULL;

    /* https://mail.python.org/pipermail/capi-sig/2010-July/000414.html */
    dv = PyString_FromString(status->channel);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "channel", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyString_FromString(status->lock_str);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "lock_str", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyBool_FromLong((long)status->signal_present);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "signal_present", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyBool_FromLong((long)status->lock_supported);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "lock_supported", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyBool_FromLong((long)status->lock_unsupported);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "lock_unsupported", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyLong_FromUnsignedLong((unsigned long)status->signal_strength);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "signal_strength", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyLong_FromUnsignedLong((unsigned long)status->signal_to_noise_quality);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "signal_to_noise_quality", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyLong_FromUnsignedLong((unsigned long)status->symbol_error_quality);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "symbol_error_quality", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyLong_FromUnsignedLong((unsigned long)status->raw_bits_per_second);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "raw_bits_per_second", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyLong_FromUnsignedLong((unsigned long)status->packets_per_second);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "packets_per_second", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    return rv;
}
