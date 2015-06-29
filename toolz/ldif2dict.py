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

import ldif
import cStringIO


class ProcessLDIF(ldif.LDIFParser, object):
    def __init__(self, input):
        super(type(self), self).__init__(input)
        self.dictionary = dict()

    def handle(self, dn, entry):
        self.dictionary[dn] = entry

    def getdict(self):
        return self.dictionary


def convert(text):
    input = cStringIO.StringIO(text)
    parser = ProcessLDIF(input)
    parser.parse()
    return parser.getdict()
