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

from skin import app_theme
from dtk.ui.draw import draw_pixbuf
from tooltip import tooltip_text
import gtk

class TopMenu(gtk.Button):
    def __init__(self, 
                 tip_text=None,
                 menu=None,
                 top_menu_normal = app_theme.get_pixbuf("top_menu/normal.png"),
                 top_menu_prelight = app_theme.get_pixbuf("top_menu/prelight.png"),
                 top_menu_press = app_theme.get_pixbuf("top_menu/press.png")
                 ):
        gtk.Button.__init__(self)
        # set topmenu tooltip.
        if tip_text:
            tooltip_text(self, tip_text)

        self.top_menu_normal = top_menu_normal
        self.top_menu_prelight = top_menu_prelight
        self.top_menu_press = top_menu_press
        self.top_menu_pixbuf_width = 40
        self.top_menu_pixbuf_height = 40
        self.menu = menu
        self.menu_show = False
        # set topmenu size.
        self.set_size_request(
            self.top_menu_pixbuf_width, 
            self.top_menu_pixbuf_height)
        # Init events.
        self.connect("expose-event", self.expose_topmenu)        
        self.connect("button-press-event", self.button_press_topmenu)
        self.connect("button-release-event", self.button_release_topmenu)
        self.connect("leave-notify-event", self.leave_notify_topmenu)
        
    def expose_topmenu(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        # get pixbuf.
        pixbuf = self.state_return_pixbuf(widget.state)
        # draw pixbuf.
        draw_pixbuf(cr,
                    pixbuf,
                    rect.x,
                    rect.y)
        return True

    def state_return_pixbuf(self, state):
        if state == gtk.STATE_NORMAL:
            return self.scale_simple(self.top_menu_normal)
        elif state == gtk.STATE_PRELIGHT:    
            return self.scale_simple(self.top_menu_prelight)
        elif state == gtk.STATE_ACTIVE:    
            return self.scale_simple(self.top_menu_press)
        
    def scale_simple(self, pixbuf):    
        return pixbuf.get_pixbuf().scale_simple(
            self.top_menu_pixbuf_width, 
            self.top_menu_pixbuf_height,
            gtk.gdk.INTERP_NEAREST)
            
    def button_press_topmenu(self, widget, event):
        self.menu_show = not self.menu_show
        
    def button_release_topmenu(self, widget, event):        
        if self.menu and self.menu_show:
            self.show_menu()
            
    def show_menu(self):            
        position = self.get_toplevel().get_position()
        rect = self.allocation
        offset_padding = 5
        offset_x = position[0] + rect.x - offset_padding
        offset_y = position[1] + self.top_menu_pixbuf_height + rect.y - offset_padding
        self.menu.show(
            (int(offset_x), int(offset_y)), 
            (0, 0))
        
    def leave_notify_topmenu(self, widget, event):    
        self.menu_show = False
