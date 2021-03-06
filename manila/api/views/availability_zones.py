# Copyright (c) 2015 Mirantis inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from manila.api import common


class ViewBuilder(common.ViewBuilder):

    _collection_name = "availability_zones"

    def _detail(self, availability_zone):
        """Detailed view of an single availability zone."""
        keys = ('id', 'name', 'created_at', 'updated_at')
        return {key: availability_zone.get(key) for key in keys}

    def detail_list(self, availability_zones):
        """Detailed view of a list of availability zones."""
        azs = [self._detail(az) for az in availability_zones]
        return {self._collection_name: azs}
