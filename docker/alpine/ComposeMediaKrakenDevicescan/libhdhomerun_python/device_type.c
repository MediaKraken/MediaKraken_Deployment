/*
 * device_type.c
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

PyDoc_STRVAR(hdhomerun_module_doc,
    "Python bindings for the SiliconDust hdhomerun library");

PyObject *hdhomerun_device_error = NULL;

int py_device_init(py_device_object *self, PyObject *args, PyObject *kwds) {
    unsigned int device_id = HDHOMERUN_DEVICE_ID_WILDCARD;
    unsigned int device_ip = 0;
    unsigned int tuner = 0;
    char *kwlist[] = {"device_ip", "device_id", "tuner", NULL};
    int success;

    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|III", kwlist, &device_ip, &device_id, &tuner))
        return -1;

    if(device_ip == 0 && device_id == HDHOMERUN_DEVICE_ID_WILDCARD) {
        PyErr_SetString(hdhomerun_device_error, "Insufficient information provided to initialize instance");
        return -1;
    }

    self->hd = hdhomerun_device_create(device_id, device_ip, 0, NULL);
    if(!self->hd) {
        PyErr_SetString(hdhomerun_device_error, "Failed to initialize Device object");
        return -1;
    }
    success = hdhomerun_device_set_tuner(self->hd, tuner);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return -1;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, "failed to set tuner number");
        return -1;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return -1;
    }
    self->locked = 0;
    return 0;
}

void py_device_dealloc(py_device_object *self) {
    if(self->locked != 0) {
        /* Try to unlock the tuner, ignore errors */
        hdhomerun_device_tuner_lockkey_release(self->hd);
        self->locked = 0;
    }
    hdhomerun_device_destroy(self->hd);
    self->hd = NULL;
    self->ob_type->tp_free((PyObject*)self);
}

uint32_t parse_ip_addr(const char *str) {
    unsigned int a[4];
    if (sscanf(str, "%u.%u.%u.%u", &a[0], &a[1], &a[2], &a[3]) != 4)
        return 0;

    return (uint32_t)((a[0] << 24) | (a[1] << 16) | (a[2] << 8) | (a[3] << 0));
}

PyDoc_STRVAR(Device_DOC_discover,
    "Locates all HDHomeRun(s) on your network and returns a list of Device objects.");

PyObject *py_device_discover(PyObject *cls, PyObject *args, PyObject *kwds) {
    PyObject *result = NULL;
    PyObject *tuner = NULL;
    char *target_ip_str = NULL;
    uint32_t target_ip = 0;
    int count = 0, i;
    char *kwlist[] = {"target_ip", NULL};
    struct hdhomerun_discover_device_t result_list[64];

    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|s", kwlist, &target_ip_str))
        return NULL;

    if(target_ip_str) {
        target_ip = parse_ip_addr(target_ip_str);
        if (target_ip == 0) {
            PyErr_SetString(hdhomerun_device_error, "invalid ip address");
            return NULL;
        }
    }

    count = hdhomerun_discover_find_devices_custom_v2(target_ip, HDHOMERUN_DEVICE_TYPE_TUNER, HDHOMERUN_DEVICE_ID_WILDCARD, result_list, 64);

    if(count < 0) {
        PyErr_SetString(hdhomerun_device_error, "error sending discover request");
        return NULL;
    }

    result = PyList_New((Py_ssize_t)count);
    if(!result) {
        return NULL;
    }

    if(count > 0) {
        for(i=0; i<count; i++) {
            tuner = PyObject_CallFunction(cls, "II", result_list[i].ip_addr, result_list[i].device_id);
            if(tuner == NULL) { Py_DECREF(result); return NULL; }
            if(PyList_SetItem(result, i, tuner) != 0) { Py_DECREF(result); return NULL; }
        }
    }

    return result;
}

PyDoc_STRVAR(Device_DOC_upgrade,
    "Uploads and installs a firmware image on a HDHomeRun device.");

PyObject *py_device_upgrade(py_device_object *self, PyObject *args, PyObject *kwds) {
    FILE *fp = NULL;
    char *filename = NULL;
    int count = 0;
    int wait = -1;
    char *version_str;
    PyObject *wait_obj = NULL;
    char *kwlist[] = {"filename", "wait", NULL};
    int success;

    if(!PyArg_ParseTupleAndKeywords(args, kwds, "sO!", kwlist, &filename, &PyBool_Type, &wait_obj))
        return NULL;
    Py_INCREF(wait_obj);
    wait = PyObject_IsTrue(wait_obj);
    Py_DECREF(wait_obj);
    if(wait < 0)
        return NULL;

    fp = fopen(filename, "rb");
    if(!fp) {
        PyErr_SetString(PyExc_IOError, "unable to open firmware file");
        return NULL;
    }
    success = hdhomerun_device_upgrade(self->hd, fp);
    fclose(fp);
    fp = NULL;
    if(success == -1) {
        PyErr_SetString(hdhomerun_device_error, "error sending upgrade file to hdhomerun device");
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, "the hdhomerun device rejected the firmware upgrade");
        return NULL;
    }

    if(wait > 0) {
        /* Wait for the device to come back online */
        msleep_minimum(10000);
        while (1) {
            if(hdhomerun_device_get_version(self->hd, &version_str, NULL) >= 0)
                break;
            count++;
            if (count > 30) {
                PyErr_SetString(hdhomerun_device_error, "error finding device after firmware upgrade");
                return NULL;
            }
            msleep_minimum(1000);
        }
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(Device_DOC_tuner_lockkey_request,
    "Locks a tuner.");

PyObject *py_device_tuner_lockkey_request(py_device_object *self) {
    char *ret_error = "the device rejected the lock request";
    int success;

    success = hdhomerun_device_tuner_lockkey_request(self->hd, &ret_error);

    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, ret_error);
        return NULL;
    } else if(success == 1) {
        self->locked = 1;
    } else {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(Device_DOC_tuner_lockkey_force,
    "Locks a tuner.");

PyObject *py_device_tuner_lockkey_force(py_device_object *self) {
    int success;

    success = hdhomerun_device_tuner_lockkey_force(self->hd);

    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, "the device rejected the forced lock request");
        return NULL;
    } else if(success == 1) {
        self->locked = 1;
    } else {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(Device_DOC_tuner_lockkey_release,
    "Unlocks a tuner.");

PyObject *py_device_tuner_lockkey_release(py_device_object *self) {
    int success;

    success = hdhomerun_device_tuner_lockkey_release(self->hd);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, "the device rejected the unlock request");
        return NULL;
    } else if(success == 1) {
        self->locked = 0;
    } else {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(Device_DOC_stream_start,
    "Tell the device to start streaming data.");

PyObject *py_device_stream_start(py_device_object *self) {
    int success;

    success = hdhomerun_device_stream_start(self->hd);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, "the device refused to start streaming");
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(Device_DOC_stream_recv,
    "Receive stream data.");

PyObject *py_device_stream_recv(py_device_object *self, PyObject *args, PyObject *kwds) {
    uint8_t *ptr;
    size_t actual_size;
    unsigned int max_size = VIDEO_DATA_BUFFER_SIZE_1S;
    char *kwlist[] = {"max_size", NULL};

    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|I", kwlist, &max_size))
        return NULL;

    ptr = hdhomerun_device_stream_recv(self->hd, (size_t)max_size, &actual_size);
    if(!ptr) {
        Py_RETURN_NONE;
    }

    return PyByteArray_FromStringAndSize((const char *)ptr, (Py_ssize_t)actual_size);
}

PyDoc_STRVAR(Device_DOC_stream_flush,
    "Undocumented.");

PyObject *py_device_stream_flush(py_device_object *self) {
    hdhomerun_device_stream_flush(self->hd);
    Py_RETURN_NONE;
}

PyDoc_STRVAR(Device_DOC_stream_stop,
    "Tell the device to stop streaming data.");

PyObject *py_device_stream_stop(py_device_object *self) {
    hdhomerun_device_stream_stop(self->hd);
    Py_RETURN_NONE;
}

PyDoc_STRVAR(Device_DOC_wait_for_lock,
    "Wait for tuner lock after channel change.");

PyObject *py_device_wait_for_lock(py_device_object *self) {
    int success;
    struct hdhomerun_tuner_status_t status;

    success = hdhomerun_device_wait_for_lock(self->hd, &status);
    if(success == -1) {
        PyErr_SetString(PyExc_IOError, DEVICE_ERR_COMMUNICATION);
        return NULL;
    } else if(success == 0) {
        PyErr_SetString(hdhomerun_device_error, "the device did not report lock status");
        return NULL;
    } else if(success != 1) {
        PyErr_SetString(hdhomerun_device_error, DEVICE_ERR_UNDOCUMENTED);
        return NULL;
    }

    return build_tuner_status_dict(&status);
}

PyDoc_STRVAR(Device_DOC_clone,
    "Clone the Device object");

PyObject *py_device_clone(py_device_object *self);

PyMethodDef py_device_methods[] = {
    /* Python methods for the Device class, not language bindings for libhdhomerun */
    {"discover",                (PyCFunction)py_device_discover,                METH_KEYWORDS | METH_CLASS, Device_DOC_discover},
    {"clone",                   (PyCFunction)py_device_clone,                   METH_NOARGS,                Device_DOC_clone},
    /* Get operations, defined in device_get.c */
    {"get_name",                (PyCFunction)py_device_get_name,                METH_NOARGS,                Device_DOC_get_name},
    {"get_device_id",           (PyCFunction)py_device_get_device_id,           METH_NOARGS,                Device_DOC_get_device_id},
    {"get_device_ip",           (PyCFunction)py_device_get_device_ip,           METH_NOARGS,                Device_DOC_get_device_ip},
    {"get_device_id_requested", (PyCFunction)py_device_get_device_id_requested, METH_NOARGS,                Device_DOC_get_device_id_requested},
    {"get_device_ip_requested", (PyCFunction)py_device_get_device_ip_requested, METH_NOARGS,                Device_DOC_get_device_ip_requested},
    {"get_tuner",               (PyCFunction)py_device_get_tuner,               METH_NOARGS,                Device_DOC_get_tuner},
    {"get_var",                 (PyCFunction)py_device_get_var,                 METH_KEYWORDS,              Device_DOC_get_var},
    {"get_tuner_status",        (PyCFunction)py_device_get_tuner_status,        METH_NOARGS,                Device_DOC_get_tuner_status},
    {"get_tuner_vstatus",       (PyCFunction)py_device_get_tuner_vstatus,       METH_NOARGS,                Device_DOC_get_tuner_vstatus},
    {"get_tuner_streaminfo",    (PyCFunction)py_device_get_tuner_streaminfo,    METH_NOARGS,                Device_DOC_get_tuner_streaminfo},
    {"get_tuner_channel",       (PyCFunction)py_device_get_tuner_channel,       METH_NOARGS,                Device_DOC_get_tuner_channel},
    {"get_tuner_vchannel",      (PyCFunction)py_device_get_tuner_vchannel,      METH_NOARGS,                Device_DOC_get_tuner_vchannel},
    {"get_tuner_channelmap",    (PyCFunction)py_device_get_tuner_channelmap,    METH_NOARGS,                Device_DOC_get_tuner_channelmap},
    {"get_tuner_filter",        (PyCFunction)py_device_get_tuner_filter,        METH_NOARGS,                Device_DOC_get_tuner_filter},
    {"get_tuner_program",       (PyCFunction)py_device_get_tuner_program,       METH_NOARGS,                Device_DOC_get_tuner_program},
    {"get_tuner_target",        (PyCFunction)py_device_get_tuner_target,        METH_NOARGS,                Device_DOC_get_tuner_target},
    {"get_tuner_plotsample",    (PyCFunction)py_device_get_tuner_plotsample,    METH_NOARGS,                Device_DOC_get_tuner_plotsample},
    {"get_tuner_lockkey_owner", (PyCFunction)py_device_get_tuner_lockkey_owner, METH_NOARGS,                Device_DOC_get_tuner_lockkey_owner},
    {"get_oob_status",          (PyCFunction)py_device_get_oob_status,          METH_NOARGS,                Device_DOC_get_oob_status},
    {"get_oob_plotsample",      (PyCFunction)py_device_get_oob_plotsample,      METH_NOARGS,                Device_DOC_get_oob_plotsample},
    {"get_ir_target",           (PyCFunction)py_device_get_ir_target,           METH_NOARGS,                Device_DOC_get_ir_target},
    {"get_version",             (PyCFunction)py_device_get_version,             METH_NOARGS,                Device_DOC_get_version},
    {"get_supported",           (PyCFunction)py_device_get_supported,           METH_KEYWORDS,              Device_DOC_get_supported},
    /* Set operations, defined in device_set.c */
    {"set_device",              (PyCFunction)py_device_set_device,              METH_KEYWORDS,              Device_DOC_set_device},
    {"set_multicast",           (PyCFunction)py_device_set_multicast,           METH_KEYWORDS,              Device_DOC_set_multicast},
    {"set_tuner",               (PyCFunction)py_device_set_tuner,               METH_KEYWORDS,              Device_DOC_set_tuner},
    {"set_tuner_from_str",      (PyCFunction)py_device_set_tuner_from_str,      METH_KEYWORDS,              Device_DOC_set_tuner_from_str},
    {"set_var",                 (PyCFunction)py_device_set_var,                 METH_KEYWORDS,              Device_DOC_set_var},
    {"set_tuner_channel",       (PyCFunction)py_device_set_tuner_channel,       METH_KEYWORDS,              Device_DOC_set_tuner_channel},
    {"set_tuner_vchannel",      (PyCFunction)py_device_set_tuner_vchannel,      METH_KEYWORDS,              Device_DOC_set_tuner_vchannel},
    {"set_tuner_channelmap",    (PyCFunction)py_device_set_tuner_channelmap,    METH_KEYWORDS,              Device_DOC_set_tuner_channelmap},
    {"set_tuner_filter",        (PyCFunction)py_device_set_tuner_filter,        METH_KEYWORDS,              Device_DOC_set_tuner_filter},
    /* Misc. operations */
    {"upgrade",                 (PyCFunction)py_device_upgrade,                 METH_KEYWORDS,              Device_DOC_upgrade},
    {"tuner_lockkey_request",   (PyCFunction)py_device_tuner_lockkey_request,   METH_NOARGS,                Device_DOC_tuner_lockkey_request},
    {"tuner_lockkey_force",     (PyCFunction)py_device_tuner_lockkey_force,     METH_NOARGS,                Device_DOC_tuner_lockkey_force},
    {"tuner_lockkey_release",   (PyCFunction)py_device_tuner_lockkey_release,   METH_NOARGS,                Device_DOC_tuner_lockkey_release},
    {"stream_start",            (PyCFunction)py_device_stream_start,            METH_NOARGS,                Device_DOC_stream_start},
    {"stream_recv",             (PyCFunction)py_device_stream_recv,             METH_KEYWORDS,              Device_DOC_stream_recv},
    {"stream_flush",            (PyCFunction)py_device_stream_flush,            METH_NOARGS,                Device_DOC_stream_flush},
    {"stream_stop",             (PyCFunction)py_device_stream_stop,             METH_NOARGS,                Device_DOC_stream_stop},
    {"wait_for_lock",           (PyCFunction)py_device_wait_for_lock,           METH_NOARGS,                Device_DOC_wait_for_lock},
    {NULL,                      NULL,                                           0,                          NULL}  /* Sentinel */
};

PyMemberDef py_device_members[] = {
    {NULL}  /* Sentinel */
};

PyDoc_STRVAR(hdhomerun_Device_type_doc,
    "An object representing a single HDHomeRun device.");

PyTypeObject hdhomerun_Device_type = {
    PyObject_HEAD_INIT(NULL)
    0,                              /* ob_size */
    "hdhomerun.Device",             /* tp_name */
    sizeof(py_device_object),       /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)py_device_dealloc,  /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_compare */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    hdhomerun_Device_type_doc,      /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    0,                              /* tp_iter */
    0,                              /* tp_iternext */
    py_device_methods,              /* tp_methods */
    py_device_members,              /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    (initproc)py_device_init,       /* tp_init */
    (allocfunc)PyType_GenericAlloc, /* tp_alloc */
    (newfunc)PyType_GenericNew,     /* tp_new */
    (freefunc)PyObject_Del,         /* tp_free */
};

PyObject *py_device_clone(py_device_object *self) {
    PyObject *arg_list, *copied_obj;
    uint32_t device_id, device_ip;
    unsigned int tuner;

    device_id = hdhomerun_device_get_device_id(self->hd);
    device_ip = hdhomerun_device_get_device_ip(self->hd);
    tuner = hdhomerun_device_get_tuner(self->hd);
    arg_list = Py_BuildValue("(III)", device_ip, device_id, tuner);
    if(arg_list == NULL) {
        return NULL;
    }
    copied_obj = PyObject_CallObject((PyObject *)&hdhomerun_Device_type, arg_list);
    Py_DECREF(arg_list);
    return copied_obj;
}

/* module methods (none for now) */
PyMethodDef hdhomerun_methods[] = {
    {NULL}  /* Sentinel */
};

PyMODINIT_FUNC inithdhomerun(void) {
    PyObject *m;

    m = Py_InitModule3("hdhomerun", hdhomerun_methods, hdhomerun_module_doc);
    if(!m)
        return;

    /* Finalize the Device type object */
    if (PyType_Ready(&hdhomerun_Device_type) < 0)
        return;
    Py_INCREF(&hdhomerun_Device_type);
    if(PyModule_AddObject(m, "Device", (PyObject *)&hdhomerun_Device_type) < 0)
        return;

    /* Initialize the DeviceError exception class */
    hdhomerun_device_error = PyErr_NewException("hdhomerun.DeviceError", PyExc_Exception, NULL);
    Py_INCREF(hdhomerun_device_error);
    if(PyModule_AddObject(m, "DeviceError", hdhomerun_device_error) < 0)
        return;
}
