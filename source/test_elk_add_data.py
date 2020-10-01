from datetime import datetime

import httpx

result = httpx.post('http://th-elk-1.beaverbay.local:9200/%s/MediaKraken'
                    % ('httpx_main_server_metadata_api_worker_themoviedb',),
                    data='{"@timestamp": "'
                         + datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                         + '", "message": "GET /search HTTP/1.1 200 1070000",'
                           ' "type": "info",'
                           ' "user": {"id": "metaman"}}',
                    headers={"Content-Type": "application/json"},
                    timeout=3.05)
print(result)
print(result.json())
