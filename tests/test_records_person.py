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

import unittest
import records.person


class TestRecordPerson(unittest.TestCase):

    def setUp(self):
        pass

    def test_typical_passwd_entry(self):
        instance = records.person.produce("bunny:8XvAVu/sWGcZQ:1344:504:Bugs Bunny,,,:/home/bbugs:/bin/bash")
        self.assertEqual(instance.username, "bunny")
        self.assertEqual(instance.uid, 1344)
        self.assertEqual(instance.gid, 504)
        self.assertEqual(instance.firstname, "Bugs")
        self.assertEqual(instance.lastname, "Bunny")
        with self.assertRaises(AttributeError):
            instance.email
        self.assertEqual(instance.password, "8XvAVu/sWGcZQ")
        self.assertEqual(instance.home, "/home/bbugs")
        self.assertEqual(instance.shell, "/bin/bash")
        self.assertEqual(instance.gecos, "Bugs Bunny,,,")
        self.assertEqual(instance.phone, "")
        self.assertEqual(instance.room,  "")
        self.assertEqual(instance.other, "")
