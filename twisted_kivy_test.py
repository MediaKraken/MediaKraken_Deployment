from common import common_docker

docker_inst = common_docker.CommonDocker()
docker_inst.com_docker_run_container('python /mediakraken/stream2chromecast/stream2chromecast.py')

docker_inst.com_docker_run_container('python /mediakraken/stream2chromecast/stream2chromecast.py'
                    + ' -devicename' + json_message['Device']
                    + subtitle_command + ' -transcodeopts -c:v copy -c:a ac3'
                    + ' -movflags faststart+empty_moov -transcode \'' + json_message['Data'] + '\'')
