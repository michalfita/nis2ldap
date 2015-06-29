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

import re
from six import iteritems


# Use https://regex101.com/#python to verify
PASSWD_REGEX = re.compile(r'(?P<_username>[^:]+):(?P<_password>[^:]*):(?P<_uid>[^:]+):(?P<_gid>[^:]+):(?P<_gecos>[^:]*):(?P<_home>[^:]*):(?P<_shell>.*)')
GECOS_REGEX = re.compile(r'(?P<_firstname>[^ ]+) (?P<_lastname>[^,]*),(?P<_room>[^,]*),(?P<_phone>[^,]*),(?P<_other>.*)')


def produce(passwd_entry):
    """
    This function converts passwd line into the Person record object.
    """
    instance = Person()
    m = PASSWD_REGEX.match(passwd_entry)
    for (k, v) in iteritems(m.groupdict()):
        if v.isdigit():
            setattr(instance, k, int(v))
        else:
            setattr(instance, k, v)
    m = GECOS_REGEX.match(instance.gecos)
    if m is None:
        return instance
    for (k, v) in iteritems(m.groupdict()):
        setattr(instance, k, v)
    return instance


class Person(object):
    """
    This class represents a person virtual recored used for conversion
    from passwd format to LDAP format.
    """

    __slots__ = ('_username', '_uid', '_gid', '_lastname', '_firstname', '_email', '_password', '_home', '_shell', '_gecos', '_phone', '_room', '_other')

    @property
    def username(self):
        return self._username

    @property
    def lastname(self):
        return self._lastname

    @property
    def firstname(self):
        return self._firstname

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def shell(self):
        return self._shell

    @property
    def uid(self):
        return self._uid

    @property
    def gid(self):
        return self._gid

    @property
    def home(self):
        return self._home

    @property
    def gecos(self):
        """
        This represents fourth field of /etc/passwd entry, that usually represents the following:
        * User's full name (or application name, if the account is for a program)
        * Building and room number or contact person
        * Office telephone number
        * Any other contact information (pager number, fax, etc.)
        """
        return self._gecos

    @property
    def phone(self):
        return self._phone

    @property
    def room(self):
        return self._room

    @property
    def other(self):
        return self._other
