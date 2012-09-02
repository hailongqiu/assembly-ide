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

from dtk.ui.utils import container_remove_all
import gtk

'''        
Toolbar 可以添加 button, image, 弹出式菜单, None, 
'''

class ToolBar(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)
        self.toolbar_list = []
        self.scale_width = 20
        self.scale_height = 20
        
    def insert(self, index, widget, tooltip_text=None):
        self.__clear_widgets()        
        if widget is None:
            widget = gtk.Label(" | ")
        self.toolbar_list.insert(index, widget)
        map(lambda toolbar_widget:self.add(toolbar_widget), self.toolbar_list)
        
    def add(self, widget):
        self.pack_start(widget, True, True)
        
    def __clear_widgets(self):    
        container_remove_all(self)
        
if __name__ == "__main__":
    from top_menu import TopMenu as Button
    win = gtk.Window()
    win.connect("destroy", lambda w : gtk.main_quit())
    
    toolbar = ToolBar()
    toolbar.insert(0, gtk.Button("编译"))
    toolbar.insert(1, gtk.Button("链接"))
    toolbar.insert(2, gtk.Button("取消"))
    toolbar.insert(2, Button("编译"))
    
    win.add(toolbar)
    win.show_all()
    gtk.main()
