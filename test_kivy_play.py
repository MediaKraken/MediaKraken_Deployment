import kivy
from kivy.app import App
from kivy.uix.behaviors import CoverBehavior
from kivy.uix.video import Video


class CoverVideo(CoverBehavior, Video):
    """Video using cover behavior.
    """

    def _on_video_frame(self, *largs):
        video = self._video
        if not video:
            return
        texture = video.texture
        self.reference_size = texture.size
        self.calculate_cover()
        self.duration = video.duration
        self.position = video.position
        self.texture = texture
        self.canvas.ask_update()


class MainApp(App):

    def build(self):
        return CoverVideo(source='big_buck_bunny_1080p_h264.mov', play=True)


if __name__ == '__main__':
    MainApp().run()
