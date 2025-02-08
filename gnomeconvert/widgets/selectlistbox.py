# selectlistbox.py
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

from pydbus import SessionBus

def open_file_manager(path):
    bus = SessionBus()
    file_manager = bus.get("org.freedesktop.FileManager1")
    file_manager.ShowFolders([f"file://{path}"], "")

open_file_manager("/home/quentin/Music")


@Gtk.Template(resource_path="/com/qsk/gconvert/SelectListbox.ui")
class SelectListbox(Gtk.ListBox):

    __gtype_name__ = 'SelectListbox'

    addbox = Gtk.Template.Child()

    def __init__(self, application):
        super().__init__()

        self.application = application

        self.filemanager = application.filemanager
        self.filemanager.connect('files-changed', self.update)

        gesture = Gtk.GestureClick()
        gesture.connect("pressed", self.load_file)  # Pas besoin de passer self.addbox ici
        self.addbox.add_controller(gesture)


    def load_file(self,gesture, n_press, x, y):
        print("cliqué")
        dialog = Gtk.FileChooserNative(title="Ouvrir un fichier", transient_for=self.application)

        filters(dialog)

        dialog.connect("response", self.add_file_2filemanager)  #self.load_response
        dialog.show()

    def add_file_2filemanager(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            active_filter = dialog.get_filter().get_name()
            print("Le filtre actif est :", active_filter)

            self.filemanager.add_file(dialog.get_file())


    def update(self, file_manager):

        for child in self.get_children():
            self.remove(child)
        for file in self.filemanager.get_files():


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
