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
import os
import subprocess

def get_installed_packages():
    try:
        # Exécutez la commande "pip freeze" via subprocess
        result = subprocess.run(['pip3', 'freeze'], capture_output=True, text=True, check=True)
        # Récupérez et retournez la sortie de la commande
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

# Appel de la fonction pour obtenir la liste des paquets installés
#installed_packages = get_installed_packages()
#print(installed_packages)

def afficher_contenu_repertoire(chemin):
    # Vérifier si le chemin spécifié est un répertoire
    if os.path.isdir(chemin):
        # Liste tous les éléments dans le répertoire
        contenu = os.listdir(chemin)

        # Afficher chaque élément
        for element in contenu:
            print(element)
    else:
        print("Le chemin spécifié n'est pas un répertoire.")

#afficher_contenu_repertoire("/app/share/gconvert/gconvert")
afficher_contenu_repertoire("/com/qsk/gconvert/")

def filters(dialog):
    # Filtre pour les images PNG, JPEG et vidéos MP4
    filter_media = Gtk.FileFilter()
    filter_media.set_name("Formats pris en charge")
    filter_media.add_mime_type("image/png")
    filter_media.add_mime_type("image/jpeg")
    filter_media.add_mime_type("video/mp4")
    filter_media.add_mime_type("video/webm")
    dialog.add_filter(filter_media)

    # Filtre pour les images PNG, JPEG et vidéos MP4
    filter_jpeg = Gtk.FileFilter()
    filter_jpeg.set_name("Images JPEG")
    filter_jpeg.add_mime_type("image/jpeg")
    dialog.add_filter(filter_jpeg)

    # Filtre pour les images PNG, JPEG et vidéos MP4
    filter_png = Gtk.FileFilter()
    filter_png.set_name("Images PNG")
    filter_png.add_mime_type("image/png")
    dialog.add_filter(filter_png)

    # Filtre pour les images PNG, JPEG et vidéos MP4
    filter_mp4 = Gtk.FileFilter()
    filter_mp4.set_name("Vidéos MP4")
    filter_mp4.add_mime_type("video/mp4")
    dialog.add_filter(filter_mp4)

    # Filtre pour les images PNG, JPEG et vidéos MP4
    filter_webm = Gtk.FileFilter()
    filter_webm.set_name("Vidéos WEBM")
    filter_webm.add_mime_type("video/webm")
    dialog.add_filter(filter_webm)

    svg_filter = Gtk.FileFilter()
    svg_filter.set_name("Fichiers SVG")
    svg_filter.add_mime_type("image/svg+xml")
    dialog.add_filter(svg_filter)

def progress_callback(progress):
    print(f'Progress: {progress:.2%}')

def find_key(valeur_cible: str, dictionnaire):
    for clé, valeur in dictionnaire.items():
        if valeur == valeur_cible:
            clé_trouvée = clé
            break
    return clé

file_formats = {"image": {"0":"image/jpg","1":"image/png","2":"image/gif","3":"image/svg"},
                "video": {"0":"video/mp4","1":"video/webm"}}

def get_children(listbox: Gtk.ListBox) -> tuple:
    ''' get all Gtk.ListBox children, just if it's a Gtk.ListBoxRow, and return a tuple '''
    children = []
    child = listbox.get_first_child()
    print(child)
    # Parcours tous les enfants de la ListBox
    while child is not None:
        if isinstance(child, Gtk.ListBoxRow):  # Vérifie si c'est un Gtk.Label
            children.append(child)
        child = child.get_next_sibling()

    return children

class ListBoxRow(Gtk.ListBoxRow):
    def __init__(self, input_file, file_format):
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

        # Créer une boîte horizontale pour contenir le Label et le ComboBox
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)# set_homogeneous=True)
        self.set_child(hbox)

        label = Gtk.Label(label=self.name)
        label.set_ellipsize(Pango.EllipsizeMode.END)  # Tronquer à la fin avec des points (...)
        #label.set_max_width_chars(10)  # Optionnel : Limiter à un certain nombre de caractères visibles
        label.set_margin_start(10)
        label.set_margin_end(10)
        label.set_margin_top(5)
        label.set_margin_bottom(5)
        label.set_hexpand(True)
        label.set_halign(Gtk.Align.START)
        hbox.append(label)

        # Créer une boîte horizontale pour contenir le Label et le ComboBox
        combobox_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)# set_homogeneous=True)
        hbox.append(combobox_box)

        combo_box = Gtk.ComboBoxText()
        if self.mime_type.startswith("image/"):
            for format in file_formats.get("image"):
                combo_box.append_text(file_formats["image"][format].split('/', 1)[1])
        if self.mime_type.startswith("video/"):
            for format in file_formats.get("video"):
                combo_box.append_text(file_formats["video"][format].split('/', 1)[1])
        combo_box.set_active(int(find_key(self.mime_type,file_formats[self.mime_type[:5]])))
        combobox_box.append(combo_box)

        label_array = Gtk.Label(label="⟶")
        combobox_box.append(label_array)

        combo_box2 = Gtk.ComboBoxText()
        if self.mime_type.startswith("image/"):
            for format in file_formats.get("image"):
                combo_box2.append_text(file_formats["image"][format].split('/', 1)[1])
        if self.mime_type.startswith("video/"):
            for format in file_formats.get("video"):
                combo_box2.append_text(file_formats["video"][format].split('/', 1)[1])
        combo_box2.set_active(int(find_key(self.mime_type,file_formats[self.mime_type[:5]])))
        combobox_box.append(combo_box2)

        #self.listbox.prepend(row)

@Gtk.Template(resource_path='/com/qsk/gconvert/window.ui')
class GconvertWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GconvertWindow'

    convert_btn = Gtk.Template.Child()
    next2 = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    listbox = Gtk.Template.Child()
    addbox = Gtk.Template.Child()
    main_contain = Gtk.Template.Child()
    convert_listbox = Gtk.Template.Child()
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

        # Ajouter un GtkGestureClick au bouton ajouter
        gesture = Gtk.GestureClick()
        gesture.connect("pressed", self.load_file, self.addbox)
        self.addbox.add_controller(gesture)

        #self.listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)

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

    #@Gtk.Template.Callback()
    def load_file(self,gesture, n_press, x, y, row):
        print("cliqué")
        dialog = Gtk.FileChooserNative(title="Ouvrir un fichier", transient_for=self)

        filters(dialog)

        dialog.connect("response", self.load_response)
        dialog.show()

    def load_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            active_filter = dialog.get_filter().get_name()
            print("Le filtre actif est :", active_filter)
            self.file = dialog.get_file()

            #print(self.file.get_path())

            #self.button1.set_label(self.file_name)

            row = ListBoxRow(self.file,"png")
            print(row.path)
            print(row.name)
            self.listbox.prepend(row)
            # Récupérer toutes les ListBoxRow de la liste box


            #self.listbox.select_all()
            #listbox_rows = self.listbox.get_selected_rows()

            #listbox_rows = self.listbox.get_first_child()
            #print(listbox_rows)

            #print("Nombre d'éléments dans la liste box :", len(listbox_rows))


            #self.listbox.unselect_all()


            self.convert_btn.set_sensitive(True)

        dialog.destroy()


