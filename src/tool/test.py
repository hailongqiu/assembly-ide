#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
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
from lang import lang, _

lang.set_lang("cn.ini")

class Test(object):
    def __init__(self):
        
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.connect("destroy", lambda w : gtk.main_quit())
        
        self.fixed = gtk.Fixed()
        self.ok_btn = gtk.Button(_(0))
        self.can_btn = gtk.Button(_(1))
        self.en_btn = gtk.Button("替换英文")
        self.en_btn.connect("clicked", self.en_btn_clicked)
        self.cn_btn = gtk.Button("替换成中文")
        self.cn_btn.connect("clicked", self.cn_btn_clicked)
        self.fixed.put(self.ok_btn, 50, 50)
        self.fixed.put(self.can_btn, 150, 50)
        self.fixed.put(self.en_btn, 250, 50)
        self.fixed.put(self.cn_btn, 380, 50)
        self.win.add(self.fixed)
        self.win.show_all()
        
    def en_btn_clicked(self, widget):
        print "en_btn_clicked.."
        lang.set_lang("en.ini")
        print "_(0):", _(0)
        self.ok_btn.set_label(_(0))
        self.can_btn.set_label(_(1))
        
    def cn_btn_clicked(self, widget):
        print "cn_btn_clicked.."
        lang.set_lang("cn.ini")
        self.ok_btn.set_label(_(0))
        self.can_btn.set_label(_(1))
        
Test()        
gtk.main()        
        

