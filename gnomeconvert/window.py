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
from gi.repository import Gtk, Gio, Pango
from PIL import Image
import ffmpeg
from gconvert import main
from gconvert.headerbar import HeaderBar
from gconvert.selectlistbox import SelectListbox
from gconvert.utils import *


@Gtk.Template(resource_path='/com/qsk/gconvert/window.ui')
class GconvertWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GconvertWindow'

    convert_btn = Gtk.Template.Child()
    next2 = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    main_contain = Gtk.Template.Child()
    convert_listbox = Gtk.Template.Child()
    toolbar_view = Gtk.Template.Child()
    '''label = Gtk.Template.Child()
    box = Gtk.Template.Child()
    button1 = Gtk.Template.Child()
    combo_box = Gtk.Template.Child()
    btn_sort = Gtk.Template.Child()
    btn_load = Gtk.Template.Child()
    convert_bar = Gtk.Template.Child()'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next2.connect("clicked", self.page1)
        '''self.box.set_orientation(Gtk.Orientation.VERTICAL)
        self.button1.connect("clicked", self.convert)
        self.combo_box.connect("changed", self.on_my_combo_box_changed)
        self.btn_load.connect('clicked', self.load_file)
        self.btn_sort.connect('clicked', self.save_file)'''

        self._headerbar = HeaderBar(self)
        #self.set_content(self._headerbar)
        self.toolbar_view.add_top_bar(self._headerbar)

        self._selectlistbox = SelectListbox(self)

        self.main_contain.append(self._selectlistbox)

        #header = HeaderBar(self)
        #box = Gtk.Box.new(1, 0)
        #box.append(header)
        #self.set_content(box)



    def page1(self, button):
        self.stack.set_visible_child_name("page1")

    @Gtk.Template.Callback()
    def convert(self, button):
        self.stack.set_visible_child_name("page2")

        children = get_children(self.listbox)

        for child in children:
            self.listbox.remove(child)
            self.convert_listbox.append(child)

            #pour créer un detecteur de progression circulaire il faudra utiliser un gtk.progressbar eet le personnalier en cercle.

            '''# Crée un Gtk.Spinner
            spinner = Gtk.Spinner()

            # Démarre l'animation
            spinner.start()

            # Ajoute le spinner à la fenêtre
            child.set_child(spinner)'''
        print(children)




