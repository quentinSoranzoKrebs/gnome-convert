# filerowbox.py
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
from gi.repository import Gtk, Gio, Pango
import os
from gconvert import main
from gconvert.filters import filters



file_formats = {"image": {"0":"image/jpg","1":"image/png","2":"image/gif","3":"image/svg"},
                "video": {"0":"video/mp4","1":"video/webm"}}


def find_key(valeur_cible: str, dictionnaire):
    for clé, valeur in dictionnaire.items():
        if valeur == valeur_cible:
            clé_trouvée = clé
            break
    return clé

@Gtk.Template(resource_path="/com/qsk/gconvert/FileRowbox.ui")
class FileRowbox(Gtk.ListBoxRow):

    __gtype_name__ = 'FileRowbox'

    hbox = Gtk.Template.Child()
    file_label = Gtk.Template.Child()
    combobox_box = Gtk.Template.Child()

    def __init__(self, application, input_file, file_format):
        super().__init__()

        self.input_file = input_file
        self.path = self.input_file.get_path()
        self.name = os.path.basename(self.path)
        self.format = file_format

        # Obtenir les métadonnées du fichier
        file_info = self.input_file.query_info("standard::*", Gio.FileQueryInfoFlags.NONE, None)
        mime_type = file_info.get_content_type()
        print(f"Type MIME : {mime_type}")

        self.mime_type = mime_type

        self.file_label.set_text(self.name)



        combo_box = Gtk.ComboBoxText()
        if self.mime_type.startswith("image/"):
            for format in file_formats.get("image"):
                combo_box.append_text(file_formats["image"][format].split('/', 1)[1])
        if self.mime_type.startswith("video/"):
            for format in file_formats.get("video"):
                combo_box.append_text(file_formats["video"][format].split('/', 1)[1])
        combo_box.set_active(int(find_key(self.mime_type,file_formats[self.mime_type[:5]])))
        self.combobox_box.append(combo_box)

        label_array = Gtk.Label(label="⟶")
        self.combobox_box.append(label_array)

        combo_box2 = Gtk.ComboBoxText()
        if self.mime_type.startswith("image/"):
            for format in file_formats.get("image"):
                combo_box2.append_text(file_formats["image"][format].split('/', 1)[1])
        if self.mime_type.startswith("video/"):
            for format in file_formats.get("video"):
                combo_box2.append_text(file_formats["video"][format].split('/', 1)[1])
        combo_box2.set_active(int(find_key(self.mime_type,file_formats[self.mime_type[:5]])))
        self.combobox_box.append(combo_box2)
