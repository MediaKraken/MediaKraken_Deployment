'''
CoreVideo implementation using libmpv with direct gl rendering in parent
context.

- Should allow using vaapi and vdpau
- Should avoid kivy having any concern about video texture upload to gpu

'''

from kivy.core.video import VideoBase
from kivy.graphics.fbo import Fbo

cdef void die(char* msg):
    print msg
    exit(0)


cdef void* get_proc_address_mpv(void* fn_ctx, const char *name):
    # XXX TODO FIXME
    return NULL


cdef class MvpPlayer(object):
    cdef Fbo fbo
    cdef mpv_handle *mpv
    cdef mpv_opengl_cb_context *mpv_gl

    # def __cinit__(self):
    #     self.fbo = NULL
    #     self.mpv = NULL
    #     self.mpv_gl = NULL

    cpdef init(self):
        self.mpv = mpv_create()
        if (not self.mpv):
            die("context init failed")

        self.mpv_gl = mpv_get_sub_api(self.mpv, MPV_SUB_API_OPENGL_CB)
        if (not self.mpv_gl):
            die("failed to create mpv GL API handle")

        # XXX get_proc_address_mpv
        if (mpv_opengl_cb_init_gl(self.mpv_gl, NULL, <void*> get_proc_address_mpv, NULL) < 0):
            die("failed to initialize mpv GL context")

        if (mpv_set_option_string(self.mpv, "vo", "opengl-cb") < 0):
            die("failed to set VO")

    cpdef play(self, char* filename):
        cdef const char **cmd = ["play", filename, NULL]
        # XXX
        if not self._fbo:
            self.load(filename)
        else:
            # XXX filename param may be unnecessary
            mpv_command(self.mpv, cmd);

    cpdef load(self, char* filename):
        cdef const char **cmd = ["loadfile", filename, NULL];
        cdef int width, height
        mpv_command(self.mpv, cmd);
        # XXX need to get video resolution, to create Fbo
        mpv_get_property(self.mpv, "width", MPV_FORMAT_DOUBLE, &width)
        mpv_get_property(self.mpv, "height", MPV_FORMAT_DOUBLE, &height)

        self.fbo = Fbo(size=(width, height))

    cpdef unload(self):
        mpv_opengl_cb_uninit_gl(self.mpv_gl);
        mpv_terminate_destroy(self.mpv);

    cpdef pause(self):
        mpv_command_string(self.mpv, "cycle pause");

    cpdef seek(self, percent):
        # XXX
        pass


class VideoMpv(VideoBase):
    '''
    '''

    def __init__(self, **kwargs):
        super(VideoMpv, self).__init__(**kwargs)
        self.player = MpvPlayer()
        self.player.init()

    def play(self):
      self.player.play(self.filename)

    def load(self):
      self.player.load(self.filename)

    def unload(self):
      self.player.unload()

    def stop(self):
      # XXX something better to do?
      self.unload()

    def pause(self):
      # XXX probably just "pause"
      self.player.pause()

    def seek(self, percent):
        self.player.seek(percent)
