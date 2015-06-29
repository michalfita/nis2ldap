# nis2ldap - Smarter NIS to LDAP synchronization tool
# Copyright (C) 2015 Michal Fita
#
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
import ldap
import ldap_access.group as lag
import records.group
import toolz.ldif2dict

from mockldap import MockLdap

# This is the content of our mock LDAP directory. We use LDIF as more readable form closer to JSON.
# It is then converted to dictonary form used by the mock.
test_ldif = """
dn: ou=Group,dc=test,dc=opensource,dc=io
objectClass: top
ou: Group

dn: cn=foobar,ou=Group,dc=test,dc=opensource,dc=io
cn: foobar
gidNumber: 266
memberUid: foobar
objectClass: posixGroup
objectClass: top
userPassword: x

dn: cn=admin,dc=test,dc=opensource,dc=io
cn: admin
objectClass: posixUser
objectClass: inetOrgPerson
objectClass: top
uid: admin
uidNumber: 666
userPassword: neptune

"""


class TestGroupLdapExport(unittest.TestCase):
    """
    Test export group records to LDAP.
    """
    base_dn = 'dc=test,dc=opensource,dc=io'
    directory = toolz.ldif2dict(test_ldif)

    @classmethod
    def setUpClass(cls):
        # We only need to create the MockLdap instance once. The content we
        # pass in will be used for all LDAP connections.
        cls.mockldap = MockLdap(cls.directory)

    @classmethod
    def tearDownClass(cls):
        del cls.mockldap

    def setUp(self):
        # Patch ldap.initialize
        self.mockldap.start()
        self.ldapobj = self.mockldap['ldap://localhost/']

    def tearDown(self):
        # Stop patching ldap.initialize and reset state.
        self.mockldap.stop()
        del self.ldapobj

    def test_check_entry_non_existing(self):
        #  self.ldapobj.simple_bind_s('cn=admin,' + self.base_dn, 'neptune')
        result = lag.check_entry(self.ldapobj, self.base_dn, 'spongebob')
        self.assertEquals(self.ldapobj.methods_called(), ['search_s'])
        self.assertEquals(result, False)

    def test_check_entry_existing(self):
        #  self.ldapobj.simple_bind_s('cn=admin,' + self.base_dn, 'neptune')
        result = lag.check_entry(self.ldapobj, self.base_dn, 'foobar')
        self.assertEquals(self.ldapobj.methods_called(), ['search_s'])
        self.assertEquals(result, True)

    def test_add_entry_non_existing(self):
        rec = records.group.produce("emperors:x:4044:bunny,duffy,roadrunner")
        result = lag.add_entry(self.ldapobj, self.base_dn, rec)
        self.assertEquals(self.ldapobj.methods_called(), ['add_s'])
        self.assertEquals(result, None)
        self.assertEquals(self.ldapobj.directory['cn=emperors,ou=Group,' + self.base_dn],
                          {'objectClass': ['posixGroup', 'top'],
                           'cn': ['emperors'],
                           'userPassword': ['x'],
                           'gidNumber': [4044],
                           'memberUid': ['bunny', 'duffy', 'roadrunner']})

    def test_add_entry_existing(self):
        rec = records.group.produce("foobar:x:266:foobar")
        with self.assertRaises(ldap.ALREADY_EXISTS):
            lag.add_entry(self.ldapobj, self.base_dn, rec)
        self.assertListEqual(self.ldapobj.methods_called(), ['add_s'])

    def test_update_entry_existing(self):
        rec = records.group.produce("foobar:x:266:foobar")
        lag.update_entry(self.ldapobj, self.base_dn, rec)

    def xxx_test_update_entry_non_existing(self):
        """
        This test cause me trouble as my experience with real LDAP is different in this
        case as I'm not getting ldap.NO_SUCH_OBJECT exception.
        """
        rec = records.group.produce("emperors:x:4044:bunny,duffy,roadrunner")
        with self.assertRaises(SystemExit) as cm:
            lag.update_entry(self.ldapobj, self.base_dn, rec)
        self.assertEquals(cm.exception.code, 200)
        self.assertListEqual(self.ldapobj.methods_called(), ['search_s'])
