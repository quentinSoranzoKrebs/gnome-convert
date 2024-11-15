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
import ffmpeg
from gconvert import main
import os
import subprocess

def get_installed_packages():
    try:
        # Exécutez la commande "pip freeze" via subprocess
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
        # Récupérez et retournez la sortie de la commande
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

# Appel de la fonction pour obtenir la liste des paquets installés
installed_packages = get_installed_packages()
print(installed_packages)

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

afficher_contenu_repertoire("/app/share/gconvert/gconvert")

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

@Gtk.Template(resource_path='/com/qsk/gconvert/window.ui')
class GconvertWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GconvertWindow'


    '''label = Gtk.Template.Child()
    box = Gtk.Template.Child()
    button1 = Gtk.Template.Child()
    combo_box = Gtk.Template.Child()
    btn_sort = Gtk.Template.Child()
    btn_load = Gtk.Template.Child()
    convert_bar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box.set_orientation(Gtk.Orientation.VERTICAL)
        self.button1.connect("clicked", self.convert)
        self.combo_box.connect("changed", self.on_my_combo_box_changed)
        self.btn_load.connect('clicked', self.load_file)
        self.btn_sort.connect('clicked', self.save_file)



    def load_file(self, button):
        dialog = Gtk.FileChooserNative(title="Ouvrir un fichier", transient_for=self)

        filters(dialog)

        dialog.connect("response", self.load_response)
        dialog.show()

    def load_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            active_filter = dialog.get_filter().get_name()
            print("Le filtre actif est :", active_filter)
            self.file = dialog.get_file()
            try:
                # Tentative d'ouverture du fichier comme une image
                with Image.open(self.file.get_path()) as img:
                    # Si l'ouverture réussit, le fichier est probablement une image
                    print("c'est une image")
                    self.combo_box.remove_all()
                    self.combo_box.append_text("png")
                    self.combo_box.append_text("jpg")
                    self.combo_box.append_text("gif")
                    self.combo_box.append_text("svg")
            except:
                # Si une erreur se produit lors de l'ouverture du fichier, il n'est pas une image
                print("ce n'est pas une image")
                self.combo_box.remove_all()
                self.combo_box.append_text("mp4")
                self.combo_box.append_text("webm")

            print(self.file.get_path())
            self.file_name = os.path.basename(self.file.get_path())
            self.button1.set_label(self.file_name)
        dialog.destroy()

    def save_response(self, dialog, response):
        self.output_path = dialog.get_file().get_path()
        print(self.output_path)

    def save_file(self,widget):
        dialog = Gtk.FileChooserNative(title="Ouvrir un fichier",action=Gtk.FileChooserAction.SAVE, transient_for=self)

        dialog.set_current_name("image.png")


        dialog.connect("response", self.save_response)
        dialog.show()

    def on_my_combo_box_changed(self,widget):
        selected_option = self.combo_box.get_active_text()
        print("Option sélectionnée :", selected_option)

    def convert(self,widget):
        self.format = self.combo_box.get_active_text()
        print(self.format)
        self.convert_vid(self.format,self.file.get_path(),self.output_path)


    def convert_img(self,form,input_image_path, output_image_path):
        self.convert_bar.set_visible(True)
        self.convert_bar.set_fraction(0.3)
        try:
            # Ouvre l'image
            with Image.open(input_image_path) as img:
                self.convert_bar.set_fraction(0.6)

                img.save(output_image_path, format=form, save_all=True, optimize=True, quality=95, progressive=True, method=3, icc_profile=None, exif=None, qtables=None, subsampling=0, quantization=0, offset=0, progress=progress)
            print("L'image a été convertie en avec succès.")
            self.convert_bar.set_fraction(1)
        except IOError:
            print("Impossible de convertir l'image.")


    def convert_vid(self,form,input_file_path, output_file_path):

        # Définition du filtre de conversion
        input_stream = ffmpeg.input(input_file_path)
        output_stream = ffmpeg.output(input_stream, output_file_path)

        # Ajout d'un callback pour afficher la progression
        output_stream = output_stream.global_args('-progress', 'pipe:1')

        # Lancer la conversion
        ffmpeg.run(output_stream)
'''
