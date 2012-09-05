#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
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
from dtk.ui.draw import draw_text
from dtk.ui.utils import get_content_size

class ComplieShowList(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)
        #
        self.set_size_request(1, 120)
        #
        self.press_index = None
        self.message_text_list = []
        self.draw_height = 20
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        
        # Init event.
        self.connect("button-press-event", self.press_complie_show_list)
        self.connect("expose-event", self.expose_complie_show_list)
        
    def add_text(self, text):    
        self.message_text_list.append(text)
        self.queue_draw()
        
    def clear_text(self):    
        self.message_text_list = []
        
    def press_complie_show_list(self, widget, event):
        press_index = int(event.y) / self.draw_height
        if press_index < len(self.message_text_list):
            self.press_index = press_index
            
        self.queue_draw()
        
    def expose_complie_show_list(self, widget, event):        
        cr = widget.window.cairo_create()
        rect = widget.allocation
        self.draw_background(cr, rect)
        
        self.draw_hight_press(cr, rect)        
        self.draw_complie_show_text(cr, rect)
        return True        
    
    def draw_background(self, cr, rect):
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(rect.x, 
                     rect.y, 
                     rect.width, 
                     rect.height)
        cr.fill()
    
    def draw_complie_show_text(self, cr, rect):    
        text_index = 0
        for text in self.message_text_list:
            offset_y = (text_index * self.draw_height)
            height = get_content_size(text)[1] + self.draw_height /2
            draw_text(cr, text, 
                      rect.x, rect.y + offset_y, 
                      rect.width, 
                      height 
                      )
            text_index += 1
            
    def draw_hight_press(self, cr, rect):
        if self.press_index is not None:
            cr.set_source_rgba(0, 0, 1, 0.6)
            cr.rectangle(rect.x, 
                         rect.y + (self.press_index * self.draw_height), 
                         rect.width, 
                         self.draw_height)
            cr.fill()
        
if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(500, 500)
    win.connect("destroy", gtk.main_quit)
    win.add(ComplieShowList())
    win.show_all()
    gtk.main()
