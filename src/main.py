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

from widget.skin import app_theme
from dtk.ui.application import Application
from dtk.ui.menu import Menu
from widget.constant import (APP_WIDTH, APP_HEIGHT)
from widget.top_menu import TopMenu as Button
from widget.toolbar import ToolBar
from widget.dialog_window import show_open_file_dialog_window
from codeedit.codeedit import CodeEdit
from tool.tool import open_gcalctool, input_link, input_bin, input_elf, run_elf
import gtk

class AssemblyIDE(object):
    def __init__ (self):            
        self.app = Application()
        # Set app size.
        self.app.set_default_size(APP_WIDTH, APP_HEIGHT)
        self.app.set_icon(app_theme.get_pixbuf("logo.ico"))
        self.app.set_skin_preview(app_theme.get_pixbuf("frame.png"))        
        # Add app titlebar.
        self.app.add_titlebar(["theme", "max", "min", "close"],
                              app_theme.get_pixbuf("logo.png"),
                              "Assembly-IDE v 1.0", " ", add_separator = True)

        self.vbox_ali = gtk.Alignment()
        self.vbox_ali.set(1, 1, 1, 1)
        self.vbox_ali.set_padding(6, 2, 2, 2)
        self.vbox = gtk.VBox()
        self.vbox_ali.add(self.vbox)

        self.init_root_menu()
        
        self.init_top_toolbar()
        
        self.code_edit = CodeEdit()
        # test code edit.
        self.code_edit_file = "/home/long/1.asm"
        self.code_edit.read(self.code_edit_file)
        
        self.vbox.pack_start(self.top_toolbar_ali, False, False)
        self.vbox.pack_start(self.code_edit, True,True)
        self.app.main_box.pack_start(self.vbox_ali, True, True)
        self.app.window.show_all()
        
    def init_root_menu(self):        
        # Init file menu.
        file_menu = Menu(
            [(None, "新建", lambda : self.code_edit.clear()), # 清空代码编辑器.
             (None, "打开", lambda : self.open_file_dialog_window()),
             (None),
             (None, "我的程序...", None),
             (None),
             (None, "保存", lambda : self.code_edit.save()),
             (None, "另存为", None),
             (None),
             (None, "退出", lambda :gtk.main_quit())
             ]
            )
        # Init edit menu.
        edit_menu = Menu(
            [(None, "剪切", None),
             (None, "复制", None),             
             (None, "粘帖", None),
             (None, "全选", None),
             (None),
             (None, "注释", lambda : self.notes_line()),
             (None, "取消注释", lambda : self.notes_line()),
             (None),
             (None, "撤销", None),
             (None, "恢复", None),
             (None),
             (None, "查找", None),
             (None, "替换", None),
             (None, "定位到行", None)
             ]
            )
        # Init run menu.
        run_menu = Menu(
            [(None, "编译成目标文件", None),
             (None, "生成可执行文件", None),
             (None, "生成动态链接库文件", None),
             (None, "运行", None),
             (None, "多模块链接", None),
             (None, "调试", None),
             (None, "运行LINUX控制台程序", None)
             ]
            )
        # Init tool menu.
        tool_menu = Menu(
            [(None, "选项", None),
             (None, "计算器", lambda :open_gcalctool())
             ]
            )
        # Init help menu.
        help_menu = Menu(
            [(None, "帮助主题", None),
             (None, "关于", None),             
             ]
            )

        # Init root menu.
        self.root_menu = Menu(
            [(None, "文件", file_menu),
             (None, "编辑", edit_menu),
             (None, "运行", run_menu),
             (None, "工具", tool_menu),
             (None, "帮助", help_menu),
             ],
            True
            )
        
    def init_top_toolbar(self):        
        self.top_toolbar_ali = gtk.Alignment()
        self.top_toolbar_ali.set(0, 0, 0, 0)
        self.top_toolbar_ali.set_padding(0, 0, 5, 0)
        self.top_toolbar = ToolBar()
        self.top_toolbar_ali.add(self.top_toolbar)
        
        
        self.bin_btn = gtk.Button("生成bin")
        self.link_btn = gtk.Button("链接")
        self.run_btn = gtk.Button("运行")        
        self.gcalctool_btn = gtk.Button("计算器")
        
        self.top_toolbar.insert(0, Button("菜单", self.root_menu))
        self.top_toolbar.insert(1, None)
        self.top_toolbar.insert(2, self.bin_btn)
        self.top_toolbar.insert(3, self.link_btn)
        self.top_toolbar.insert(4, self.run_btn)
        self.top_toolbar.insert(5, None)
        self.top_toolbar.insert(6, self.gcalctool_btn)
        
        
        self.bin_btn.connect("clicked", self.bin_btn_clicked)
        self.link_btn.connect("clicked", self.link_btn_clicked)
        self.run_btn.connect("clicked", self.run_btn_clicked)
        self.gcalctool_btn.connect("clicked", self.gcalctool_btn_clicked)
        
    def bin_btn_clicked(self, widget):
        pass
    
    def link_btn_clicked(self, widget):        
        print input_link(self.code_edit_file, "/home/long/1.o")
        
    def run_btn_clicked(self, widget):    
        run_bool = input_elf("/home/long/1.o", "/home/long/test.out")
        if run_bool == "编译完成":
            run_elf("/home/long/test.out")
        
    def gcalctool_btn_clicked(self, widget):
        open_gcalctool()
        
    def open_file_dialog_window(self):    
        open_file_path = show_open_file_dialog_window()
        if open_file_path:
            self.code_edit.read(open_file_path)
            
    def notes_line(self):        
        self.code_edit.cursor_start_insert_ch()
        
AssemblyIDE()
gtk.main()
