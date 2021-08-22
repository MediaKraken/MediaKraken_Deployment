
    def process_message(self, server_msg):
        """
        Process network message from server
        """
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={"body": server_msg})
        # network_base.NetworkEvents.ampq_message_received(body)
        json_message = json.loads(server_msg)
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'json body': json_message})
        msg = None
        if json_message['Type'] == "Ident":
            msg = "VALIDATE " + "link" + " " + "password" + " " + platform.node()
        elif json_message['Type'] == "Receive New Media":
            for new_media in json_message['Data']:
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         'new_media': new_media})
                # returns: 0-mm_media_guid, 1-'Movie', 2-mm_media_ffprobe_json,
                # 3-mm_metadata_media_id jsonb
                metadata_guid = None
                if new_media[1] == common_global.DLMediaType.Movie.value:
                    metadata_guid = self.db_connection.db_meta_guid_by_imdb(
                        new_media[3]['imdb'])
                    if metadata_guid is None:
                        metadata_guid = self.db_connection.db_meta_guid_by_tmdb(
                            new_media[3]['themoviedb'])
                        if metadata_guid is None:
                            metadata_guid = self.db_connection.db_meta_guid_by_tvdb(
                                new_media[3]['thetvdb'])
                elif new_media[1] == common_global.DLMediaType.TV.value:
                    metadata_guid \
                        = self.db_connection.db_metatv_guid_by_imdb(new_media[3]['imdb'])
                    if metadata_guid is None:
                        metadata_guid = self.db_connection.db_metatv_guid_by_tvmaze(
                            new_media[3]['tvmaze'])
                        if metadata_guid is None:
                            metadata_guid = self.db_connection.db_metatv_guid_by_tvdb(
                                new_media[3]['thetvdb'])
                elif new_media[1] == 'Sports':
                    metadata_guid = self.db_connection.db_metasports_guid_by_thesportsdb(
                        new_media[3]['thesportsdb'])
                elif new_media[1] == common_global.DLMediaType.Music.value:
                    pass
                elif new_media[1] == common_global.DLMediaType.Publication_Book.value:
                    pass
                if metadata_guid is None:
                    # find on internet
                    # for "keys" in new_media[3]
                    pass
                self.db_connection.db_insert_remote_media(json_message['Target'], new_media[0],
                                                          new_media[1],
                                                          new_media[2],
                                                          metadata_guid)
            self.db_connection.db_commit()
        else:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'stuff': 'unknown message type'})
        if msg is not None:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'stuff': 'should be sending data'})
            networkProtocol.sendString(msg)
