/*
 * device_common.h
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

#ifndef _DEVICE_COMMON_H
#define _DEVICE_COMMON_H

#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include <Python.h>
#include <structmember.h>
#include <libhdhomerun/hdhomerun.h>

typedef struct {
    PyObject_HEAD
    struct hdhomerun_device_t *hd;
    unsigned int locked;
} py_device_object;

/* Defined in device_type.c */
extern PyObject *hdhomerun_device_error;

/* Defined in device_common.c */
PyObject *build_tuner_status_dict(struct hdhomerun_tuner_status_t *);

/* String constants for use when raising exceptions */
extern const char * const DEVICE_ERR_REJECTED_OP;
extern const char * const DEVICE_ERR_COMMUNICATION;
extern const char * const DEVICE_ERR_UNDOCUMENTED;

/* Defined in device_get.c */

extern const char Device_DOC_get_name[];
PyObject *py_device_get_name(py_device_object *);

extern const char Device_DOC_get_device_id[];
PyObject *py_device_get_device_id(py_device_object *);

extern const char Device_DOC_get_device_ip[];
PyObject *py_device_get_device_ip(py_device_object *);

extern const char Device_DOC_get_device_id_requested[];
PyObject *py_device_get_device_id_requested(py_device_object *);

extern const char Device_DOC_get_device_ip_requested[];
PyObject *py_device_get_device_ip_requested(py_device_object *);

extern const char Device_DOC_get_tuner[];
PyObject *py_device_get_tuner(py_device_object *);

extern const char Device_DOC_get_var[];
PyObject *py_device_get_var(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_get_tuner_status[];
PyObject *py_device_get_tuner_status(py_device_object *);

extern const char Device_DOC_get_tuner_vstatus[];
PyObject *py_device_get_tuner_vstatus(py_device_object *);

extern const char Device_DOC_get_tuner_streaminfo[];
PyObject *py_device_get_tuner_streaminfo(py_device_object *);

extern const char Device_DOC_get_tuner_channel[];
PyObject *py_device_get_tuner_channel(py_device_object *);

extern const char Device_DOC_get_tuner_vchannel[];
PyObject *py_device_get_tuner_vchannel(py_device_object *);

extern const char Device_DOC_get_tuner_channelmap[];
PyObject *py_device_get_tuner_channelmap(py_device_object *);

extern const char Device_DOC_get_tuner_filter[];
PyObject *py_device_get_tuner_filter(py_device_object *);

extern const char Device_DOC_get_tuner_program[];
PyObject *py_device_get_tuner_program(py_device_object *);

extern const char Device_DOC_get_tuner_target[];
PyObject *py_device_get_tuner_target(py_device_object *);

extern const char Device_DOC_get_tuner_plotsample[];
PyObject *py_device_get_tuner_plotsample(py_device_object *);

extern const char Device_DOC_get_tuner_lockkey_owner[];
PyObject *py_device_get_tuner_lockkey_owner(py_device_object *);

extern const char Device_DOC_get_oob_status[];
PyObject *py_device_get_oob_status(py_device_object *);

extern const char Device_DOC_get_oob_plotsample[];
PyObject *py_device_get_oob_plotsample(py_device_object *);

extern const char Device_DOC_get_ir_target[];
PyObject *py_device_get_ir_target(py_device_object *);

extern const char Device_DOC_get_version[];
PyObject *py_device_get_version(py_device_object *);

extern const char Device_DOC_get_supported[];
PyObject *py_device_get_supported(py_device_object *, PyObject *, PyObject *);

/* Defined in device_set.c */

extern const char Device_DOC_set_device[];
PyObject *py_device_set_device(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_set_multicast[];
PyObject *py_device_set_multicast(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_set_tuner[];
PyObject *py_device_set_tuner(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_set_tuner_from_str[];
PyObject *py_device_set_tuner_from_str(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_set_var[];
PyObject *py_device_set_var(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_set_tuner_channel[];
PyObject *py_device_set_tuner_channel(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_set_tuner_vchannel[];
PyObject *py_device_set_tuner_vchannel(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_set_tuner_channelmap[];
PyObject *py_device_set_tuner_channelmap(py_device_object *, PyObject *, PyObject *);

extern const char Device_DOC_set_tuner_filter[];
PyObject *py_device_set_tuner_filter(py_device_object *, PyObject *, PyObject *);

#endif /* _DEVICE_COMMON_H */
