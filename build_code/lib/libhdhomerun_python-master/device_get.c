/*
 * device_get.c
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

/*
 *  Functions which operate directly on the hdhomerun_device_t pointer
 */

const char Device_DOC_get_name[] = "Get the device name.";
PyObject *py_device_get_name(py_device_object *self) {
    const char *name;

    name = hdhomerun_device_get_name(self->hd);
    return PyString_FromString(name);
}

const char Device_DOC_get_device_id[] = "Get the device ID.";
PyObject *py_device_get_device_id(py_device_object *self) {
    uint32_t device_id;

    device_id = hdhomerun_device_get_device_id(self->hd);
    return PyLong_FromUnsignedLong((unsigned long)device_id);
}

const char Device_DOC_get_device_ip[] = "Get the device IP.";
PyObject *py_device_get_device_ip(py_device_object *self) {
    uint32_t device_ip;

    device_ip = hdhomerun_device_get_device_ip(self->hd);
    return PyLong_FromUnsignedLong((unsigned long)device_ip);
}

const char Device_DOC_get_device_id_requested[] = "Get the requested device ID.";
PyObject *py_device_get_device_id_requested(py_device_object *self) {
    uint32_t device_id;

    device_id = hdhomerun_device_get_device_id_requested(self->hd);
    return PyLong_FromUnsignedLong((unsigned long)device_id);
}

const char Device_DOC_get_device_ip_requested[] = "Get the requested device IP.";
PyObject *py_device_get_device_ip_requested(py_device_object *self) {
    uint32_t device_ip;

    device_ip = hdhomerun_device_get_device_ip_requested(self->hd);
    return PyLong_FromUnsignedLong((unsigned long)device_ip);
}

const char Device_DOC_get_tuner[] = "Get the tuner number that this Device object references.";
PyObject *py_device_get_tuner(py_device_object *self) {
    unsigned int tuner_number;

    tuner_number = hdhomerun_device_get_tuner(self->hd);
    return PyLong_FromUnsignedLong((unsigned long)tuner_number);
}

/*
 *  Functions which operate on a HDHomeRun device
 */

const char Device_DOC_get_var[] = "Get a named control variable on the device.";
PyObject *py_device_get_var(py_device_object *self, PyObject *args, PyObject *kwds) {
    char *ret_value = NULL;
    char *ret_error = "the get operation was rejected by the device";
    char *item = NULL;
    int success;
    char *kwlist[] = {"item", NULL};

    if(!PyArg_ParseTupleAndKeywords(args, kwds, "s", kwlist, &item))
        return NULL;

    success = hdhomerun_device_get_var(self->hd, item, &ret_value, &ret_error);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, ret_error);
        return NULL;
    } else if(success == 1) {
        return PyString_FromString(ret_value);
    } else {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }
}

const char Device_DOC_get_tuner_status[] = "Get the tuner's status";
PyObject *py_device_get_tuner_status(py_device_object *self) {
    int success;
    char *pstatus_str;
    struct hdhomerun_tuner_status_t status;

    success = hdhomerun_device_get_tuner_status(self->hd, &pstatus_str, &status);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    /*
     *  pstatus_str is a string that represents a subset of the structure contents,
     *  which might look like this:
     *    ch=qam:549000000 lock=qam256 ss=100 snq=91 seq=100 bps=13215648 pps=0
     *  We can ignore it here since we return the complete contents of the struct as a dict.
     */
    return build_tuner_status_dict(&status);
}

const char Device_DOC_get_tuner_vstatus[] = "Get the tuner's vstatus";
PyObject *py_device_get_tuner_vstatus(py_device_object *self) {
    PyObject *rv, *dv;
    int success;
    char *pvstatus_str;
    struct hdhomerun_tuner_vstatus_t vstatus;

    success = hdhomerun_device_get_tuner_vstatus(self->hd, &pvstatus_str, &vstatus);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    /*
     *  pvstatus_str is a string that represents a subset of the structure contents,
     *  which might look like this:
     *    vch=702 name=KTVUD auth=unspecified cci=none
     *  We can ignore it here since we return the complete contents of the struct as a dict.
     */
    rv = PyDict_New();
    if(!rv) return NULL;

    dv = PyString_FromString(vstatus.vchannel);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "vchannel", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyString_FromString(vstatus.name);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "name", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyString_FromString(vstatus.auth);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "auth", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyString_FromString(vstatus.cci);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "cci", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyString_FromString(vstatus.cgms);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "cgms", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyBool_FromLong((long)vstatus.not_subscribed);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "not_subscribed", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyBool_FromLong((long)vstatus.not_available);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "not_available", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    dv = PyBool_FromLong((long)vstatus.copy_protected);
    if(!dv) { Py_DECREF(rv); return NULL; }
    if(PyDict_SetItemString(rv, "copy_protected", dv) != 0) { Py_DECREF(rv); return NULL; }
    Py_DECREF(dv);

    return rv;
}

const char Device_DOC_get_tuner_streaminfo[] = "Get the tuner's stream info";
PyObject *py_device_get_tuner_streaminfo(py_device_object *self) {
    int success;
    char *pstreaminfo = NULL;

    success = hdhomerun_device_get_tuner_streaminfo(self->hd, &pstreaminfo);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(pstreaminfo);
}

const char Device_DOC_get_tuner_channel[] = "Get the tuner's channel";
PyObject *py_device_get_tuner_channel(py_device_object *self) {
    int success;
    char *pchannel = NULL;

    success = hdhomerun_device_get_tuner_channel(self->hd, &pchannel);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(pchannel);
}

const char Device_DOC_get_tuner_vchannel[] = "Get the tuner's vchannel";
PyObject *py_device_get_tuner_vchannel(py_device_object *self) {
    int success;
    char *pvchannel = NULL;

    success = hdhomerun_device_get_tuner_vchannel(self->hd, &pvchannel);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(pvchannel);
}

const char Device_DOC_get_tuner_channelmap[] = "Get the tuner's channel map";
PyObject *py_device_get_tuner_channelmap(py_device_object *self) {
    int success;
    char *pchannelmap = NULL;

    success = hdhomerun_device_get_tuner_channelmap(self->hd, &pchannelmap);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(pchannelmap);
}

const char Device_DOC_get_tuner_filter[] = "Get the tuner's filter";
PyObject *py_device_get_tuner_filter(py_device_object *self) {
    int success;
    char *pfilter = NULL;

    success = hdhomerun_device_get_tuner_filter(self->hd, &pfilter);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(pfilter);
}

const char Device_DOC_get_tuner_program[] = "Get the tuner's program";
PyObject *py_device_get_tuner_program(py_device_object *self) {
    int success;
    char *pprogram = NULL;

    success = hdhomerun_device_get_tuner_program(self->hd, &pprogram);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(pprogram);
}

const char Device_DOC_get_tuner_target[] = "Get the tuner's target";
PyObject *py_device_get_tuner_target(py_device_object *self) {
    int success;
    char *ptarget = NULL;

    success = hdhomerun_device_get_tuner_target(self->hd, &ptarget);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(ptarget);
}


const char Device_DOC_get_tuner_plotsample[] = "Get the tuner's plot sample";
PyObject *py_device_get_tuner_plotsample(py_device_object *self) {
    int success, i;
    size_t pcount;
    struct hdhomerun_plotsample_t *psamples = NULL;
    PyObject *sample_list, *sample;

    success = hdhomerun_device_get_tuner_plotsample(self->hd, &psamples, &pcount);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    sample_list = PyList_New((Py_ssize_t)pcount);
    if(!sample_list)
        return NULL;
    if(pcount == 0)
        return sample_list;
    for(i=0; i<pcount; i++) {
        sample = PyComplex_FromDoubles((double)psamples[i].real, (double)psamples[i].imag);
        if(sample == NULL) {
            Py_DECREF(sample_list);
            return NULL;
        }
        if(PyList_SetItem(sample_list, (Py_ssize_t)i, sample) != 0) {
            Py_DECREF(sample_list);
            return NULL;
        }
    }
    return sample_list;
}

const char Device_DOC_get_tuner_lockkey_owner[] = "Get the tuner's lock owner";
PyObject *py_device_get_tuner_lockkey_owner(py_device_object *self) {
    int success;
    char *powner = NULL;

    success = hdhomerun_device_get_tuner_lockkey_owner(self->hd, &powner);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(powner);
}

const char Device_DOC_get_oob_status[] = "Get the device's OOB status";
PyObject *py_device_get_oob_status(py_device_object *self) {
    int success;
    char *pstatus_str;
    struct hdhomerun_tuner_status_t status;

    success = hdhomerun_device_get_oob_status(self->hd, &pstatus_str, &status);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return build_tuner_status_dict(&status);
}

const char Device_DOC_get_oob_plotsample[] = "Get the OOB plot sample";
PyObject *py_device_get_oob_plotsample(py_device_object *self) {
    int success, i;
    size_t pcount;
    struct hdhomerun_plotsample_t *psamples = NULL;
    PyObject *sample_list, *sample;

    success = hdhomerun_device_get_oob_plotsample(self->hd, &psamples, &pcount);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    sample_list = PyList_New((Py_ssize_t)pcount);
    if(!sample_list)
        return NULL;
    if(pcount == 0)
        return sample_list;
    for(i=0; i<pcount; i++) {
        sample = PyComplex_FromDoubles((double)psamples[i].real, (double)psamples[i].imag);
        if(sample == NULL) {
            Py_DECREF(sample_list);
            return NULL;
        }
        if(PyList_SetItem(sample_list, (Py_ssize_t)i, sample) != 0) {
            Py_DECREF(sample_list);
            return NULL;
        }
    }
    return sample_list;
}

const char Device_DOC_get_ir_target[] = "Get the device's IR target";
PyObject *py_device_get_ir_target(py_device_object *self) {
    int success;
    char *ptarget = NULL;

    success = hdhomerun_device_get_ir_target(self->hd, &ptarget);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(ptarget);
}

const char Device_DOC_get_version[] = "Get the device's firmware version";
PyObject *py_device_get_version(py_device_object *self) {
    int success;
    uint32_t version_num;
    char *pversion_str = NULL;

    success = hdhomerun_device_get_version(self->hd, &pversion_str, &version_num);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return Py_BuildValue("(sk)", pversion_str, version_num);
}

const char Device_DOC_get_supported[] = "Get supported";
PyObject *py_device_get_supported(py_device_object *self, PyObject *args, PyObject *kwds) {
    int success;
    char *pstr = NULL;
    char *prefix = NULL;
    char *kwlist[] = {"prefix", NULL};

    if(!PyArg_ParseTupleAndKeywords(args, kwds, "s", kwlist, &prefix))
        return NULL;

    success = hdhomerun_device_get_supported(self->hd, prefix, &pstr);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_REJECTED_OP);
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return PyString_FromString(pstr);
}
