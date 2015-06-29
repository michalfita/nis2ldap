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
from __future__ import print_function

import ldap
import ldap.cidict
import ldap.filter
import ldap.modlist
import sys


def record2entry(record):
    """
    Mutates record into entry dictionary understandable by the library.
    """
    return ldap.cidict.cidict({
        'objectClass': ['posixGroup', 'top'],
        'cn': ['%s' % (record.groupname)],
        'userPassword': [record.password],
        'gidNumber': [record.gid],
        'memberUid': record.members
    })


def check_entry(ldap_conn, base_dn, groupname):
    """
    Checks if group exist in the LDAP database.
    """
    search_dn = 'ou=Group,' + base_dn
    filter = ldap.filter.filter_format('(cn=%s)', [groupname])
    result = ldap_conn.search_s(search_dn, ldap.SCOPE_SUBTREE, filter, None)  # ['uid', 'uidNumber'])
    if result is None or len(result) == 0:
        return False
    else:
        # print result
        return True


def add_entry(ldap_conn, base_dn, record):
    """
    Simply add group entry into the LDAP database.
    """
    insert_dn = 'cn=%s,ou=Group,%s' % (record.groupname, base_dn)
    modlist = ldap.modlist.addModlist(record2entry(record))
    ldap_conn.add_s(insert_dn, modlist)


def update_entry(ldap_conn, base_dn, record):
    """
    Applies changes to the group entry in the LDAP database.
    """
    update_dn = 'cn=%s,ou=Group,%s' % (record.groupname, base_dn)
    filter = ldap.filter.filter_format('(cn=%s)', [record.groupname])
    result = ldap_conn.search_s(update_dn, ldap.SCOPE_BASE, filter, None)
    if result is None or len(result) == 0:
        print("Group not found.", file = sys.stderr)
        exit(100)
    elif len(result) != 1:
        print("Multiple entries for group found!", file = sys.stderr)
        print("Result: %s" % result, file = sys.stderr)
        exit(200)
    origentry = result[0][1]  # First tuple on result list, second element in tuple
    modlist = ldap.modlist.modifyModlist(origentry, record2entry(record))
    ldap_conn.modify_s(update_dn, modlist)


if __name__ == '__main__':
    import collections
    GroupRecord = collections.namedtuple('GroupRecord', 'groupname, gid, password, members')
    ldap_conn = ldap.open('gitlab.dev.bluearc.com')
    base_dn = 'dc=dev,dc=bluearc,dc=com'
    ldap_conn.simple_bind_s('cn=admin,' + base_dn, 'nasadmin')
    print(check_entry(ldap_conn, base_dn, 'mfita'))
    record = GroupRecord(groupname='foobar', gid='2666', password='x', members = ['foobar'])
    # add_entry(ldap_conn, base_dn, record)
    update_entry(ldap_conn, base_dn, record)
