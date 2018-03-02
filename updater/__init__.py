#
# foris-controller
# Copyright (C) 2018 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#


import os
import subprocess
import json

RUNNING_FILE_PATH = "/tmp/updater-running-mock"
APPROVAL_FILE_PATH = "/tmp/updater-approval-mock.json"


def is_running():
    return os.path.exists(RUNNING_FILE_PATH)


def get_approval():
    if not os.path.exists(APPROVAL_FILE_PATH):
        return None
    with open(APPROVAL_FILE_PATH) as f:
        return json.load(f)


def resolve_approval(approval_id, grant):
    """ resolve approval

    :param approval_id: id of the approval
    :type approval_id: string
    :param grant: shall the approval be granted otherwise it will be denied
    :type grant: bool
    """
    # try to find approval
    try:
        with open(APPROVAL_FILE_PATH) as f:
            data = json.load(f)
    except Exception:
        return False

    # check and update status
    if data["id"] != approval_id or data["status"] != "asked":
        return False
    data["status"] = "granted" if grant else "denied"

    # write it back
    try:
        with open(APPROVAL_FILE_PATH, "w") as f:
            data = json.dump(data, f)
            f.flush()
    except Exception:
        return False

    return True


def run(set_reboot_indicator):
    subprocess.Popen(["python", "-m", "updater"] + (["-p"] if set_reboot_indicator else []))
    return True
