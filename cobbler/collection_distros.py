"""
A distro represents a network bootable matched set of kernels
and initrd files

Copyright 2006, Red Hat, Inc
Michael DeHaan <mdehaan@redhat.com>

This software may be freely redistributed under the terms of the GNU
general public license.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""

import utils
import collection
import item_distro as distro
from cexceptions import *
import action_litesync
from rhpl.translate import _, N_, textdomain, utf8

TESTMODE = False

class Distros(collection.Collection):

    def collection_type(self):
        return "distro"

    def factory_produce(self,config,seed_data):
        """
        Return a Distro forged from seed_data
        """
        return distro.Distro(config).from_datastruct(seed_data)

    def filename(self):
        """
        Config file for distro serialization
        """
        if TESTMODE:
            return "/var/lib/cobbler/test/distros"
        else:
            return "/var/lib/cobbler/distros"

    def remove(self,name,with_delete=False):
        """
        Remove element named 'name' from the collection
        """
        name = name.lower()
        # first see if any Groups use this distro
        for v in self.config.profiles():
            if v.distro == name:
               raise CX(_("removal would orphan profile: %s") % v.name)
        if self.find(name=name):
            if with_delete:
                self._run_triggers(self.listing[name], "/var/lib/cobbler/triggers/delete/distro/pre/*")
                lite_sync = action_litesync.BootLiteSync(self.config)
                lite_sync.remove_single_profile(name)
                self._run_triggers(self.listing[name], "/var/lib/cobbler/triggers/delete/distro/post/*")
            del self.listing[name]
            return True
        raise CX(_("cannot delete object that does not exist"))

