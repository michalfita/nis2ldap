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

import ldap
import ldap.cidict
import ldap.filter
import ldap.modlist


def record2entry(record):
    """
    Mutates record into entry dictionary understandable by the library.
    """
    return ldap.cidict.cidict({
        'uid': record.username,
        'objectClass': ['person', 'organizationalPerson', 'inetOrgPerson', 'posixAccount', 'top'],
        'sn': record.lastname,
        'cn': '%s %s' % (record.firstname, record.lastname),
        'givenName': record.firstname,
        'mail': record.email,
        'userPassword': record.password,
        'loginShell': record.shell,
        'uidNumber': record.uid,
        'gidNumber': record.gid,
        'homeDirectory': record.home,
        'gecos': record.gecos
    })


def check_entry(ldap_conn, base_dn, username):
    """
    Checks if user exist in the LDAP database.
    """
    search_dn = 'ou=People,' + base_dn
    filter = ldap.filter.filter_format('(uid=%s)', [username])
    result = ldap_conn.search_s(search_dn, ldap.SCOPE_SUBTREE, filter, None)  # ['uid', 'uidNumber'])
    if result is None or len(result) == 0:
        return False
    else:
        # print result
        return True


def add_entry(ldap_conn, base_dn, record):
    """
    Simply add user entry into the LDAP database.
    """
    insert_dn = 'uid=%s,ou=People,%s' % (record.username, base_dn)
    # entry = ('uid=%s,%s' % (record.username, insert_dn), record2entry(record))
    modlist = ldap.modlist.addModlist(record2entry(record))  # entry)
    ldap_conn.add_s(insert_dn, modlist)


def update_entry(ldap_conn, base_dn, record):
    """
    Applies changes to the user entry in the LDAP database.
    """
    update_dn = 'uid=%s,ou=People,%s' % (record.username, base_dn)
    filter = ldap.filter.filter_format('(uid=%s)', [record.username])
    result = ldap_conn.search_s(update_dn, ldap.SCOPE_BASE, filter, None)
    if result is None or len(result) == 0:
        print "User not found."
        exit(100)
    elif len(result) != 1:
        print "Multple entries for user found!"
        exit(200)
    print result
    origentry = result[0][1]  # First tuple on result list, second element in tuple
    # entry = ('uid=%s,%s' % (record.username, update_dn), record2entry(record))
    modlist = ldap.modlist.modifyModlist(origentry, record2entry(record))
    ldap_conn.modify_s(update_dn, modlist)


if __name__ == '__main__':
    import collections
    PersonRecord = collections.namedtuple('PersonRecord', 'username, uid, gid, firstname, lastname, email, password, shell, home, gecos')
    ldap_conn = ldap.open('gitlab.dev.bluearc.com')
    base_dn = 'dc=dev,dc=bluearc,dc=com'
    ldap_conn.simple_bind_s('cn=admin,' + base_dn, 'nasadmin')
    print check_entry(ldap_conn, base_dn, 'mfita')
    record = PersonRecord(username='foobar', uid='2666', gid='2666', lastname='Bar', firstname='Foo', email='mike@foobar.com', password='unclear', shell='/usr/bin/zsh', home='/home/foobar', gecos='Foo Bar,,,')
    # add_entry(ldap_conn, base_dn, record)
    update_entry(ldap_conn, base_dn, record)
