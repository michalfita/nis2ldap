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

import re
from six import iteritems


GROUP_REGEX = re.compile(r'(?P<_groupname>[^:]+):(?P<_password>[^:]*):(?P<_gid>[^:]*):(?P<_members>.*)')


def produce(group_entry):
    instance = Group()
    m = GROUP_REGEX.match(group_entry)
    for (k, v) in iteritems(m.groupdict()):
        if v.isdigit():
            setattr(instance, k, int(v))
        else:
            setattr(instance, k, v)
    return instance


class Group(object):
    """
    This class represents a person virtual recored used for conversion
    from passwd format to LDAP format.
    """

    __slot__ = ('_groupname', '_password', '_gid', '_members')

    @property
    def groupname(self):
        return self._groupname

    @property
    def password(self):
        return self._password

    @property
    def gid(self):
        return self._gid

    @property
    def members(self):
        return self._members.split(',')
