import kivy
from kivy.app import App
from kivy.uix.behaviors import CoverBehavior
from kivy.uix.video import Video


class MyApp(App):
    def build(self):
        #video = Video(source='/home/spoot/github/MediaKraken_Deployment/A.mkv')
        video = Video(source='/home/spoot/github/MediaKraken_Deployment/big_buck_bunny_1080p_h264.mov')
        video.state='play'
        video.options = {'eos': 'loop'}
        video.allow_stretch=True
        return video

if __name__ == '__main__':
    MyApp().run()
