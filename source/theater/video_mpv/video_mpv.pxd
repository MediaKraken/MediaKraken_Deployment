from kivy.core.video import VideoBase
from kivy.graphics.fbo cimport Fbo


cdef extern from "mpv/client.h":
    ctypedef struct mpv_handle
    cdef mpv_handle* mpv_create()
    cdef int mpv_set_option_string(mpv_handle*, char*, char*)
    cdef int mpv_command(mpv_handle*, const char**)
    cdef void mpv_terminate_destroy(mpv_handle*)
    cdef int mpv_get_property(mpv_handle*, const char *name, mpv_format, void*)
    cdef int mpv_command_string(mpv_handle *ctx, const char *args);
    cdef int MPV_FORMAT_DOUBLE = 5


cdef extern from "mpv/opengl_cb.h":
    ctypedef struct mpv_opengl_cb_context
    cdef mpv_opengl_cb_context* mpv_get_sub_api(mpv_handle*, int)
    cdef int mpv_opengl_cb_init_gl(mpv_opengl_cb_context*, void*, void*, void*)
    cdef int mpv_opengl_cb_uninit_gl(mpv_opengl_cb_context*)
    cdef int MPV_SUB_API_OPENGL_CB = 1


cdef class MpvPlayer(object):
    cdef Fbo fbo
    cdef mpv_handle *mpv
    cdef mpv_opengl_cb_context *mpv_gl