
    @wait_for(timeout=5.0)
    def connect_to_server(self):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'stuff': 'conn server'})
        if self.config is not None:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'stuff': 'here in connect to server'})
            if self.config.get('MediaKrakenServer', 'Host').strip() == 'None':
                # TODO if more than one server, popup list selection
                server_list = common_network_mediakraken.com_net_mediakraken_find_server()
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         'server list': server_list})
                host_ip = server_list[0].decode()  # as this is returned as bytes
                # TODO allow pick from list and save it below
                self.config.set('MediaKrakenServer', 'Host',
                                host_ip.split(':')[0])
                self.config.set('MediaKrakenServer', 'Port',
                                host_ip.split(':')[1])
                with open(r'mediakraken.ini', 'wb') as configfile:
                    self.config.write()
            else:
                pass
            reactor.connectSSL(self.config.get('MediaKrakenServer', 'Host').strip(),
                               int(self.config.get(
                                   'MediaKrakenServer', 'Port').strip()),
                               MKFactory(), ssl.ClientContextFactory())

    @wait_for(timeout=5.0)
    def send_twisted_message(self, message):
        """
        Send message via twisted reactor
        """
        if twisted_connection is not None:
            MKFactory.protocol.sendline_data(twisted_connection, message)

    def send_twisted_message_thread(self, message):
        """
        Send message via twisted reactor from the crochet thread
        """
        if twisted_connection is not None:
            MKFactory.protocol.sendline_data(twisted_connection, message)

    def process_message(self, server_msg):
        """
        Process network message from server
        """
        json_message = json.loads(server_msg.decode())
        try:
            if json_message['Type'] != "Image":
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         "Got Message": server_msg})
            else:
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         "Got Image Message":
                                                                             json_message[
                                                                                 'Subtype'],
                                                                         'uuid':
                                                                             json_message['UUID']})
        except:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                "full record": server_msg})
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            "len total": len(server_msg)})
        # determine message type and work to be done
        if json_message['Type'] == "Ident":
            # Send a uuid for this connection. This way same installs can be copied, etc.
            # and not run into each other.
            self.send_twisted_message_thread(json.dumps({'Type': 'Ident',
                                                         'UUID': str(uuid.uuid4()),
                                                         'Platform': platform.node()}))
            # start up the image refresh since we have a connection
            Clock.schedule_interval(self.main_image_refresh, 5.0)

        elif json_message['Type'] == 'Play':  # direct file play
            video_source_dir = json_message['Data']
            # TODO - load real mapping
            share_mapping = (
                ('/mediakraken/mnt/', '/home/spoot/zfsspoo/Media/'),)
            if share_mapping is not None:
                for mapping in share_mapping:
                    video_source_dir = video_source_dir.replace(mapping[0], mapping[1])
            if os.path.exists(video_source_dir):
                # direct play it
                self.mpv_process = subprocess.Popen(
                    shlex.split(
                        'mpv --no-config --fullscreen --ontop --no-osc --no-osd-bar --aid=2',
                        '--audio-spdif=ac3,dts,dts-hd,truehd,eac3 --audio-device=pulse',
                        '--hwdec=auto --input-ipc-server ./mk_mpv.sock \"'
                        + video_source_dir + '\"'), stdout=subprocess.PIPE, shell=False)
                self.mpv_connection = common_network_mpv.CommonNetMPVSocat()
        elif json_message['Type'] == "Image":
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'stuff': "here for movie refresh"})
            if json_message['Image Media Type'] == "Demo":
                f = open("./image_demo", "w")
                f.write(str(base64.b64decode(json_message['Data'])))
                f.close()
                self.demo_media_id = json_message['UUID']
                if self.first_image_demo == False:
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                         message_text={
                                                                             'stuff': 'boom'})
                    self.root.ids.main_home_demo_image.reload()
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                         message_text={
                                                                             'stuff': 'boom2'})
                else:
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                         message_text={
                                                                             'stuff': 'wha2'})
                    proxy_image_demo = Loader.image("./image_demo")
                    proxy_image_demo.bind(
                        on_load=self._image_loaded_home_demo)
                    self.first_image_demo = False
        elif json_message['Type'] == "MPV":
            # sends the data message direct as a command to local running mpv
            self.mpv_connection.execute(json_message['Data'])
        else:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='error', message_text={'stuff': "unknown message type"})

    def build_config(self, config):
        """
        Build base config
        """
        config.setdefaults('MediaKrakenServer', {
            'Host': 'None',
            'Port': 8903})
        config.setdefaults('Audio', {
            'Default_Device': 'Default',
            'Channels': '7.1'})
        config.setdefaults('Passthrough', {
            'Enable': False,
            'Device': 'Default',
            'DTS': False,
            'DTSHD': False,
            'DTSX': False,
            'AC3': False,
            'EAC3': False,
            'TRUEHD': False,
            'Atmos': False})
        config.setdefaults('MediaKraken', {
            'Default_Device': 'Default'})
        config.setdefaults('Video', {
            'Blank_Displays': False,
            'Display_Screen': 'Display #1',
            'Resolution': 'Window Size',
            'Fullscreen': True,
            'Fullscreen_Window': False,
            'Sleep_Time': '3 min'})
        config.setdefaults('Library', {
            'Show_Plot_Unwatched': True,
            'Flatten_TV_Show_Seasons': 'If Only One Season',
            'Group_Movies_in_Sets': True})
        config.setdefaults('Playback', {
            'Preferred_Audio_Language': 'Original Stream Language',
            'Play_Next_Media_Automatically': False})

    def build_settings(self, settings):
        settings.add_json_panel('MediaKraken', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_base_json)
        settings.add_json_panel('Audio', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_audio_json)
        settings.add_json_panel('Video', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_video_json)
        settings.add_json_panel('Library', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_library_json)
        settings.add_json_panel('Playback', self.config,
                                data=MediaKrakenSettings.mediakraken_settings_playback_json)

    def on_config_change(self, config, section, key, value):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'config': config,
                                                                           'section': section,
                                                                           'key': key, 'value':
                                                                               value})

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            "keycode received": keycode})
        if keycode[1] == 'backspace':
            if self.root.ids._screen_manager.current == 'Main_Theater_Home':
                pass
        elif keycode[1] == 'escape':
            sys.exit()
        elif keycode[1] == 'f1':
            # display help
            pass
        return True

    def theater_event_button_user_select_login(self, *args):
        self.dismiss_popup()
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            "button server user login":
                self.global_selected_user_id})
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            "login": self.login_password})
        self.send_twisted_message(json.dumps({'Type': 'Login',
                                              'User': self.global_selected_user_id,
                                              'Password': self.login_password}))
        self.root.ids._screen_manager.current = 'Main_Remote'

    # in order from the KV file
    def main_mediakraken_event_button_home(self, *args):
        msg = json.dumps({'Type': 'Media', 'Subtype': 'List', 'Data': args[0]})
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={"home press": args})
        if args[0] == 'in_progress' or args[0] == 'recent_addition' \
                or args[0] == 'movie' or args[0] == 'video':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Video_List'
        elif args[0] == 'demo':
            # add movie id to stream
            try:
                msg += " " + self.demo_media_id
                self.root.ids._screen_manager.current = 'Main_Theater_Media_Playback'
            except:
                msg = None
        else:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='error', message_text={'stuff': "unknown button event"})
        if msg is not None:
            self.send_twisted_message(msg)

    def theater_event_button_option_select(self, option_text, *args):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            "button server options": option_text})
        if option_text == 'Audio Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Audio'
        elif option_text == 'Playback Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Playback'
        elif option_text == 'Video Settings':
            self.root.ids._screen_manager.current = 'Main_Theater_Media_Settings_Video'

    # send refresh for images
    def main_image_refresh(self, *largs):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'stuff': "image refresh"})
        # if main page refresh all images
        if self.root.ids._screen_manager.current == 'Main_Theater_Home':
            # refreshs for movie stuff
            # request main screen background refresh
            self.send_twisted_message(json.dumps({'Type': 'Image', 'Subtype': 'Movie',
                                                  'Image Media Type': 'Demo',
                                                  'Image Type': 'Backdrop'}))

    def _image_loaded_home_demo(self, proxyImage):
        """
        Load home image
        """
        if proxyImage.image.texture:
            self.root.ids.main_home_demo_image.texture = proxyImage.image.texture
        # don't bother now.....as it's always the same name and will be reloaded
        # since it's loaded delete the image
        # os.remove('./image_demo')


if __name__ == '__main__':
    # for windows exe support
    from multiprocessing import freeze_support

    freeze_support()
    # start logging
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text='START',
                                                         index_name='main_theater_thin')

    # set signal exit breaks
    common_signal.com_signal_set_break()

    log.startLogging(sys.stdout)  # for twisted

    # load the kivy's here so all the classes have been defined
    Builder.load_file('theater_thin/kivy_layouts/main.kv')
    Builder.load_file('theater_resources/kivy_layouts/KV_Layout_Notification.kv')
    if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
        pass  # as os.uname doesn't exist in windows
    else:
        # so the raspberry pi doesn't crash
        if os.uname()[4][:3] != 'arm':
            Window.fullscreen = 'auto'
    MediaKrakenApp().run()
