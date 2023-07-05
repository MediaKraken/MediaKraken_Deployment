
    def on_message(self, _unused_channel, basic_deliver, properties, body):
        if body is not None:
            common_logging_elasticsearch_httpx.com_es_httpx_post(
                message_type='info',
                message_text={'msg body': body})
            json_message = json.loads(body)
            if json_message['Type'] == 'Hardware':
                if json_message['Subtype'] == 'Lights':
                    if json_message['Hardware'] == 'Hue':
                        hardware_hue = common_hardware_hue.CommonHardwareHue(json_message['Target'])
                        if json_message['Action'] == 'OnOff':
                            hardware_hue.com_hardware_hue_light_set(json_message['LightList'], 'on',
                                                                    json_message['Setting'])
                        elif json_message['Action'] == 'Bright':
                            hardware_hue.com_hardware_hue_light_set(json_message['LightList'],
                                                                    'bri',
                                                                    json_message['Setting'])
            elif json_message['Type'] == 'Hardware Scan':
                hardware_proc = subprocess.Popen('/mediakraken/main_hardware_discover.py',
                                                 stdout=subprocess.PIPE,
                                                 shell=False)
                # hardware_proc.wait()  # do NOT wait, as it's blocking
        self.acknowledge_message(basic_deliver.delivery_tag)
