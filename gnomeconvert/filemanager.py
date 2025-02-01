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
from PIL import Image
import ffmpeg

class FileManager(GObject.GObject):

    __gsignals__ = {
        'files-changed': (GObject.SignalFlags.RUN_FIRST, None, ()),
        "file-converted": (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    def __init__(self, application):
        super().__init__()
        self.files = []

    def convert_all(self, callback=None):
        """
        Convert and save all files in the self.files and saved
        with a new name in the same directory as the original file.
        """
        for i, file in enumerate(self.files):
            try:
                # Get the original image path
                path = file.get_path()

                # Open the image
                with Image.open(path) as image:
                    # Convert the image to RGB mode (removes alpha channel)
                    image_rgb = image.convert('RGB')

                    # Create a new file path with the same name but .jpg extension
                    base_name = os.path.splitext(os.path.basename(path))[0]  # Get filename without extension
                    new_img_path = os.path.join(os.path.dirname(path), f"{base_name}.jpg")

                    # Save the converted image in JPEG format
                    image_rgb.save(new_img_path, 'JPEG')
                    #print(f"Converted and saved: {new_img_path}")

                progress = (i + 1) / len(self.files) if len(self.files) > 0 else 1.0


                if callback:
                    callback(file, "success", progress)   # return callback to confirm conversion and inform about progress


            except Exception as e:
                print(f"Failed to convert {path}: {e}")

                if callback:
                    callback(file, f"error: {e}", None)  # Inform UI about error



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
