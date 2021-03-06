# Copyright (c) 2015 Mirantis inc.
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

import ddt
import mock

from manila.api.v1 import availability_zones
from manila import context
from manila import test
from manila.tests.api import fakes


@ddt.ddt
class AvailabilityZonesAPITest(test.TestCase):

    def test_instantiate_controller(self):
        controller = availability_zones.AvailabilityZoneController()

        self.assertTrue(hasattr(controller, "resource_name"))
        self.assertEqual("availability_zone", controller.resource_name)
        self.assertTrue(hasattr(controller, "_view_builder"))
        self.assertTrue(hasattr(controller._view_builder, "detail_list"))

    @ddt.data('1.0', '2.0', '2.6')
    def test_index(self, version):
        azs = [
            {
                "id": "fake_id1",
                "name": "fake_name1",
                "created_at": "fake_created_at",
                "updated_at": "fake_updated_at",
            },
            {
                "id": "fake_id2",
                "name": "fake_name2",
                "created_at": "fake_created_at",
                "updated_at": "fake_updated_at",
                "deleted": "False",
                "redundant_key": "redundant_value",
            },
        ]
        self.mock_object(availability_zones.db, 'availability_zone_get_all',
                         mock.Mock(return_value=azs))
        controller = availability_zones.AvailabilityZoneController()
        ctxt = context.RequestContext("admin", "fake", True)
        req = fakes.HTTPRequest.blank('/shares', version=version)
        req.environ['manila.context'] = ctxt

        result = controller.index(req)

        availability_zones.db.availability_zone_get_all.\
            assert_called_once_with(ctxt)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(["availability_zones"], list(result.keys()))
        self.assertTrue(isinstance(result["availability_zones"], list))
        self.assertEqual(2, len(result["availability_zones"]))
        self.assertTrue(azs[0] in result["availability_zones"])
        azs[1].pop("deleted")
        azs[1].pop("redundant_key")
        self.assertTrue(azs[1] in result["availability_zones"])
