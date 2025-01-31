# convertlistbox.py
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

from gconvert import main
from gconvert.filters import filters
from gconvert.widgets.filerowbox import FileRowbox


@Gtk.Template(resource_path="/com/qsk/gconvert/ConvertListbox.ui")
class ConvertListbox(Gtk.ListBox):

    __gtype_name__ = 'ConvertListbox'

    def __init__(self, application):
        super().__init__()

        self.application = application

        self._filemanager = application._filemanager
        self._filemanager.connect('files-changed', self.update)

        '''gesture = Gtk.GestureClick()
        gesture.connect("pressed", self.fonction)
        self.addbox.add_controller(gesture)'''

    def update(self, file_manager):

        for child in self.get_children():
            self.remove(child)
        for file in self._filemanager.get_files():


            row = FileRowbox(self, file,"png")
            #print(row.path)
            #print(row.name)
            self.prepend(row)

            self.application.convert_btn.set_sensitive(True)


    def get_children(self) -> tuple:
        ''' get all Gtk.ListBox children, just if it's a Gtk.ListBoxRow, and return a tuple '''
        children = []
        child = self.get_first_child()
        print(child)
        # Parcours tous les enfants de la ListBox
        while child is not None:
            if isinstance(child, FileRowbox):  # Vérifie si c'est un Gtk.Label
                children.append(child)
            child = child.get_next_sibling()

        return children

    def on_files_changed(self, file_manager):
        print("La liste des fichiers a changé. Mettre à jour l'affichage.")
        # Mettre à jour l'interface utilisateur ici
