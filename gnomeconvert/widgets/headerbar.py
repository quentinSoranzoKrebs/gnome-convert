# headerbar.py
#
# Copyright 2024 quentin
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
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk, Gio
from gconvert import main


@Gtk.Template(resource_path="/com/qsk/gconvert/HeaderBar.ui")
class HeaderBar(Adw.Bin):

    __gtype_name__ = 'HeaderBar'

    def __init__(self, application):
        super().__init__()
