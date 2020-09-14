import os
import platform
from os.path import sep, expanduser, dirname

from kivy.app import App
from kivy.factory import Factory
from kivy.garden.filebrowser import FileBrowser
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.utils import platform


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            # common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
            #                                         {'stuff': "selection changed to {0}".format(
            #                                             rv.data[index])})
            # if twisted_connection is not None:
            #     MKFactory.protocol.sendline_data(twisted_connection,
            #                                      json.dumps({'Type': 'Media', 'Subtype': 'Detail',
            #                                                  'UUID': rv.data[index]['uuid']}))
            # common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff': rv.data[index]['path']})
            MainRenamer.media_path = rv.data[index]['path']
            MainRenamer.media_uuid = rv.data[index]['uuid']


class CustomDropDown(DropDown):
    pass


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Output Directory", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)
        self.dismiss_popup()


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
            on_success=self.fbrowser_success,
            on_canceled=self.fbrowser_canceled)
        return browser

    def fbrowser_canceled(self, instance):
        print('cancelled, Close self.', flush=True)

    def fbrowser_success(self, instance):
        print(instance.selection, flush=True)


Factory.register('Root', cls=Root)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    MainRenamer().run()
