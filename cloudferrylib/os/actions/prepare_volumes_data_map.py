# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.


from cloudferrylib.base.action import action
from cloudferrylib.utils import utils as utl
import copy


class PrepareVolumesDataMap(action.Action):

    def __init__(self, src_vol_info_name, dst_vol_info_name):
        self.src_vol_info_name = src_vol_info_name
        self.dst_vol_info_name = dst_vol_info_name
        super(PrepareVolumesDataMap, self).__init__()

    def run(self, **kwargs):
        volumes_data_map = {}
        src_vol_info = kwargs[self.src_vol_info_name]
        dst_vol_info = kwargs[self.dst_vol_info_name]
        src_storage_info = copy.deepcopy(src_vol_info)
        src_volumes = src_storage_info[utl.STORAGE_RESOURCE][utl.VOLUMES_TYPE]
        dst_storage_info = copy.deepcopy(dst_vol_info)
        dst_volumes = dst_storage_info[utl.STORAGE_RESOURCE][utl.VOLUMES_TYPE]

        for id, vol in dst_volumes.iteritems():
            src_id = vol[utl.OLD_ID]
            src_host = src_volumes[src_id][utl.VOLUME_BODY]['host']
            src_path = src_volumes[src_id][utl.VOLUME_BODY]['path']
            dst_host = vol[utl.VOLUME_BODY]['host']
            dst_path = vol[utl.VOLUME_BODY]['path']
            volumes_data_map[id] = {
                utl.OLD_ID: src_id,
                utl.VOLUME_BODY: {
                    utl.SRC_HOST: src_host,
                    utl.SRC_PATH: src_path,
                    utl.DST_HOST: dst_host,
                    utl.DST_PATH: dst_path
                }
            }
            volumes = {
                utl.STORAGE_RESOURCE: {
                    utl.VOLUMES_TYPE: volumes_data_map
                }
            }

        return {
            'storage_info': volumes
        }