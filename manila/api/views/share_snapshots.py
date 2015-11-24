# Copyright 2013 NetApp
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
from manila.common import constants


class ViewBuilder(common.ViewBuilder):
    """Model a server API response as a python dictionary."""

    _collection_name = 'snapshots'

    def summary_list(self, request, snapshots):
        """Show a list of share snapshots without many details."""
        return self._list_view(self.summary, request, snapshots)

    def detail_list(self, request, snapshots):
        """Detailed view of a list of share snapshots."""
        return self._list_view(self.detail, request, snapshots)

    def summary(self, request, snapshot):
        """Generic, non-detailed view of an share snapshot."""
        return {
            'snapshot': {
                'id': snapshot.get('id'),
                'name': snapshot.get('display_name'),
                'links': self._get_links(request, snapshot['id'])
            }
        }

    def detail(self, request, snapshot):
        """Detailed view of a single share snapshot."""

        """if snapshot status cannot be queried"""
        """its instance should be deleted"""
        snapshot_status = snapshot.get('status')
        if snapshot_status is None:
            snapshot_status = constants.STATUS_DELETING

        return {
            'snapshot': {
                'id': snapshot.get('id'),
                'share_id': snapshot.get('share_id'),
                'share_size': snapshot.get('share_size'),
                'created_at': snapshot.get('created_at'),
                'status': snapshot_status,
                'name': snapshot.get('display_name'),
                'description': snapshot.get('display_description'),
                'size': snapshot.get('size'),
                'share_proto': snapshot.get('share_proto'),
                'links': self._get_links(request, snapshot['id'])
            }
        }

    def _list_view(self, func, request, snapshots):
        """Provide a view for a list of share snapshots."""
        snapshots_list = [func(request, snapshot)['snapshot']
                          for snapshot in snapshots]
        snapshots_links = self._get_collection_links(request,
                                                     snapshots,
                                                     self._collection_name)
        snapshots_dict = {self._collection_name: snapshots_list}

        if snapshots_links:
            snapshots_dict['share_snapshots_links'] = snapshots_links

        return snapshots_dict
