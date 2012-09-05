#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import os

def get_home_path():
    return os.path.expanduser("~")    

def show_open_file_dialog_window(title_text="代码编辑器"):
    open_dialog = gtk.FileChooserDialog(
        title_text,
        None,
        gtk.FILE_CHOOSER_ACTION_OPEN,
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    
    open_dialog.set_current_folder(get_home_path())
    res = open_dialog.run()
    if res == gtk.RESPONSE_OK:
        path_string = open_dialog.get_filename()
        open_dialog.destroy()
        return path_string
    else:
        open_dialog.destroy()
        
