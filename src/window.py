# window.py
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
from gi.repository import Gtk
from PIL import Image
import os

@Gtk.Template(resource_path='/com/qsk/gconvert/window.ui')
class GconvertWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GconvertWindow'

    liste = Gtk.Template.Child()
    Global_box = Gtk.Template.Child()
    btn = Gtk.Template.Child()
    my_combobox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.liste.set_text("Nouveau texte")
        self.Global_box.set_orientation(Gtk.Orientation.VERTICAL)
        self.btn.connect("clicked", self.on_button_clicked1)
        self.my_combobox.append_text("Option 1")
        self.my_combobox.connect("changed", self.on_my_combo_box_changed)
        self.button = Gtk.Button(label='Ouvrir un fichier')
        self.button.connect('clicked', self.on_open_file_button_clicked)
        self.Global_box.append(self.button)

    def on_open_file_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog(title="Ouvrir un fichier", transient_for=self)
        dialog.add_button("Annuler", Gtk.ResponseType.CANCEL)
        dialog.add_button("Ouvrir", Gtk.ResponseType.ACCEPT)
        dialog.connect("response", self.on_file_chooser_response)
        dialog.show()

    def on_file_chooser_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.file = dialog.get_file()
            print(self.file.get_path())
            self.file_name = os.path.basename(self.file.get_path())
            self.button.set_label(self.file_name)
        dialog.destroy()


    def on_button_clicked1(self,widget):
        image = Image.open(self.file.get_path())
        # Convertir l'image en noir et blanc
        image_bw = image.convert('L')

        # Définir le chemin de sauvegarde pour l'image convertie
        output_directory = "/home/quentin/Images"
        output_filename = "image_convertie.jpg"
        output_path = os.path.join(output_directory, output_filename)
        # Enregistrer l'image convertie dans le répertoire spécifié
        image_bw.save(output_path)

    def on_button_clicked2(self,widget):
        self.Global_box.set_orientation(Gtk.Orientation.VERTICAL)

    def on_my_combo_box_changed(self,widget):
        selected_option = self.my_combobox.get_active_text()
        print("Option sélectionnée :", selected_option)

