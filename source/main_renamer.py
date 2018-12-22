import platform
from os.path import sep, expanduser, dirname

from kivy.app import App
from kivy.garden.filebrowser import FileBrowser
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


# class Root(FloatLayout):
#     loadfile = ObjectProperty(None)
#     savefile = ObjectProperty(None)
#     text_input = ObjectProperty(None)
#
#     def dismiss_popup(self):
#         self._popup.dismiss()
#
#     def show_load(self):
#         content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
#         self._popup = Popup(title="Input Directory", content=content,
#                             size_hint=(0.9, 0.9))
#         self._popup.open()
#
#     def show_save(self):
#         content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
#         self._popup = Popup(title="Output Directory", content=content,
#                             size_hint=(0.9, 0.9))
#         self._popup.open()
#
#     def load(self, path, filename):
#         with open(os.path.join(path, filename[0])) as stream:
#             self.text_input.text = stream.read()
#         self.dismiss_popup()
#
#     def save(self, path, filename):
#         with open(os.path.join(path, filename), 'w') as stream:
#             stream.write(self.text_input.text)
#         self.dismiss_popup()


class MainRenamer(App):
    def build(self):
        self.title = 'MediaKraken Media Renamer'
        # icon = 'custom-kivy-icon.png'
        if platform == 'win':
            user_path = dirname(expanduser('~')) + sep + 'Documents'
        else:
            user_path = expanduser('~') + sep + 'Documents'
        browser = FileBrowser(select_string='Select',
                              dirselect=True,
                              multiselect=True,
                              favorites=[(user_path, 'Documents')])
        browser.bind(
            on_success=self._fbrowser_success,
            on_canceled=self._fbrowser_canceled)
        return browser

    def _fbrowser_canceled(self, instance):
        print('cancelled, Close self.')

    def _fbrowser_success(self, instance):
        print(instance.selection)


# Factory.register('Root', cls=Root)
# Factory.register('LoadDialog', cls=LoadDialog)
# Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    MainRenamer().run()
