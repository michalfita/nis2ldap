# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import unittest
import records.group


class TestRecordGroup(unittest.TestCase):
    """
    Simple test case showing production of correct group record.
    """
    def setUp(self):
        pass

    def test_typical_group_entry(self):
        instance = records.group.produce("emperors:x:4044:bunny,duffy,roadrunner")
        self.assertEqual(instance.groupname, "emperors")
        self.assertEqual(instance.password, 'x')
        self.assertEqual(instance.gid, 4044)
        self.assertEqual(instance.members, ["bunny", "duffy", "roadrunner"])
