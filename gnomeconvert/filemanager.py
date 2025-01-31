# filemanager.py
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

from gi.repository import Gtk, Gio, GLib, GObject
import os

class FileManager(GObject.GObject):

    __gsignals__ = {
        'files-changed': (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, application):
        super().__init__()
        self.files = []

    def convert(self, file, input_format, output_format):
        pass

    def read_file(self):
        pass

    def write_file(self):
        pass

    def detect_format(self, file) -> str:
        pass

    def get_files(self) -> list :
        return self.files

    def add_file(self, file) -> None :
        self.files.append(file)
        print(self.files)
        self.emit('files-changed')
