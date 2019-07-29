from common import common_file
from common import common_network
from common import common_logging_elasticsearch
from common import common_global
import os
import json
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('zztest')

# file_name = 'http://files.tmdb.org/p/exports/movie_ids_07_27_2019.json.gz'
# common_network.mk_network_fetch_from_url(file_name, 'movie.gz')

json_data = common_file.com_file_ungzip('movie.gz').decode('utf-8')
for json_row in json_data.splitlines(keepends=True):
   print(json.loads(json_row)['id'])
   break

'''
{"adult":false,"id":601,"original_title":"E.T. the Extra-Terrestrial","popularity":18.373,"video":false}
{"adult":false,"id":602,"original_title":"Independence Day","popularity":20.256,"video":false}
{"adult":false,"id":603,"original_title":"The Matrix","popularity":30.207,"video":false}
{"adult":false,"id":604,"original_title":"The Matrix Reloaded","popularity":18.195,"video":false}
{"adult":false,"id":605,"original_title":"The Matrix Revolutions","popularity":18.061,"video":false}
{"adult":false,"id":606,"original_title":"Out of Africa","popularity":10.07,"video":false}
{"adult":false,"id":607,"original_title":"Men in Black","popularity":26.757,"video":false}
{"adult":false,"id":608,"original_title":"Men in Black II","popularity":26.805,"video":false}
'''
