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

from gconvert.utils import *
from gi.repository import Adw
from gi.repository import Gtk, Gio, Pango

from gconvert import main
from gconvert.widgets.headerbar import HeaderBar
from gconvert.widgets.selectlistbox import SelectListbox
from gconvert.widgets.convertlistbox import ConvertListbox
from gconvert.filemanager import FileManager

@Gtk.Template(resource_path='/com/qsk/gconvert/window.ui')
class GconvertWindow(Adw.ApplicationWindow):

    __gtype_name__ = 'GconvertWindow'

    convert_btn = Gtk.Template.Child()
    next2 = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    main_contain = Gtk.Template.Child()
    toolbar_view = Gtk.Template.Child()
    listbox_contain = Gtk.Template.Child()
    convertbox_contain = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next2.connect("clicked", self.page1)

        self.filemanager = FileManager(self)


        self._headerbar = HeaderBar(self)
        #self.set_content(self._headerbar)
        self.toolbar_view.add_top_bar(self._headerbar)

        self.selectlistbox = SelectListbox(self)
        self.listbox_contain.append(self.selectlistbox)

        self.convertlistbox = ConvertListbox(self)
        self.convertbox_contain.append(self.convertlistbox)



    def page1(self, button):
        self.stack.set_visible_child_name("page1")


    @Gtk.Template.Callback()
    def convert(self, button):
        self.stack.set_visible_child_name("page2")

        self.filemanager.convert_all(self.on_conversion_progress)


        #pour créer un detecteur de progression circulaire il faudra utiliser un gtk.progressbar eet le personnalier en cercle.

        '''# Crée un Gtk.Spinner
        spinner = Gtk.Spinner()

        # Démarre l'animation
        spinner.start()

        # Ajoute le spinner à la fenêtre
        child.set_child(spinner)'''



    def on_conversion_progress(self, file, status, progress):
        """Callback appelé après chaque fichier converti."""
        if status == "success":
            print(f"✅ Conversion réussie : {file}")
            self.progress_bar.set_fraction(progress)

        elif "error" in status:
            print(f"❌ Erreur sur {file} : {status}")

